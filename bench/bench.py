#!/usr/bin/env python3
"""Does a skill change what the agent delivers, and what it costs?

One task, one hidden check per thing that was asked. Every arm gets the same
model, the same frozen repository and the same request; only the skill text
differs. Checks live outside the directory the agent works in.

  python3 bench.py validate
  python3 bench.py run --harness claude --model claude-sonnet-5-5 --out runs/mine
  python3 bench.py summarize runs/mine
"""
from __future__ import annotations
import argparse, base64, getpass, hashlib, json, os, random, re, shutil, statistics, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASKS = ROOT / "tasks"
ARMS = json.loads((ROOT / "arms.json").read_text())
CACHE = ROOT / ".arms"

RUNNER = r"""
import importlib.util, json, sys, unittest
spec = importlib.util.spec_from_file_location("_hidden", sys.argv[1])
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
out = {}
for case in unittest.defaultTestLoader.loadTestsFromModule(module):
    for test in case:
        result = unittest.TestResult()
        test.run(result)
        out[test.id().rsplit(".", 1)[-1]] = result.wasSuccessful()
print("\n@@RESULT@@" + json.dumps(out))
"""


def sh(argv, cwd=None, timeout=None):
    # stdin is closed: Pi's print mode waits on an inherited stdin and never starts.
    return subprocess.run(argv, cwd=cwd, text=True, capture_output=True, timeout=timeout, stdin=subprocess.DEVNULL)


def arm_text(name: str) -> str:
    """The exact text an arm adds to the system prompt. External skills are fetched by blob SHA and verified."""
    arm = ARMS[name]
    if "text" in arm:
        return arm["text"]
    if "path" in arm:
        return (ROOT / arm["path"]).read_text()
    cached = CACHE / f"{name}.md"
    if not cached.exists():
        out = sh(["gh", "api", f"repos/{arm['repository']}/git/blobs/{arm['blob_sha']}", "--jq", ".content"])
        if out.returncode:
            raise RuntimeError(f"cannot fetch {name}: {out.stderr}")
        CACHE.mkdir(exist_ok=True)
        cached.write_bytes(base64.b64decode(out.stdout))
    data = cached.read_bytes()
    if hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest() != arm["blob_sha"]:
        raise RuntimeError(f"{name}: blob SHA mismatch")
    return data.decode()


def agent_command(args, arm_file: Path | None) -> list[str]:
    """Headless agent with no user settings, skills, extensions or MCP servers: only the arm text differs."""
    if args.harness == "claude":
        argv = ["claude", "-p", "--model", args.model, "--setting-sources", "", "--strict-mcp-config", "--disable-slash-commands",
                "--no-session-persistence", "--permission-mode", "bypassPermissions", "--output-format", "json"]
        return argv + (["--append-system-prompt-file", str(arm_file)] if arm_file else [])
    argv = ["pi", "-p", "--mode", "json", "--model", args.model, "--thinking", args.thinking,
            "--no-skills", "--no-context-files", "--no-extensions", "--no-session"]
    return argv + (["--append-system-prompt", str(arm_file)] if arm_file else [])


def usage(harness: str, stdout: str) -> dict:
    """Token, cost and turn totals from the harness's own JSON output."""
    tokens = {"input": 0, "output": 0, "cacheRead": 0, "cost": 0.0}
    turns = tools = 0
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        if harness == "claude" and event.get("type") == "result":
            used = event.get("usage") or {}
            tokens["input"] += used.get("input_tokens", 0) + used.get("cache_creation_input_tokens", 0)
            tokens["output"] += used.get("output_tokens", 0)
            tokens["cacheRead"] += used.get("cache_read_input_tokens", 0)
            tokens["cost"] += event.get("total_cost_usd") or 0
            turns += event.get("num_turns", 0)
        elif harness == "pi" and event.get("type") == "tool_execution_start":
            tools += 1
        elif harness == "pi" and event.get("type") == "message_end" and (event.get("message") or {}).get("usage"):
            used = event["message"]["usage"]
            turns += 1
            for key in ("input", "output", "cacheRead"):
                tokens[key] += used.get(key, 0)
            tokens["cost"] += (used.get("cost") or {}).get("total", 0)
    tokens["cost"] = round(tokens["cost"], 6)
    return {"tokens": tokens, "turns": turns, **({"tool_calls": tools} if harness == "pi" else {})}


def load(task: Path) -> dict:
    return json.loads((task / "task.json").read_text())


def clone(task: Path, dest: Path, meta: dict):
    sh(["git", "clone", "-q", str(task / "baseline.bundle"), str(dest)])
    sh(["git", "checkout", "-q", meta["baseline_sha"]], dest)
    sh(["git", "remote", "remove", "origin"], dest)


def score(repo: Path, task: Path, meta: dict) -> dict:
    """Run every hidden check on its own; a crash or hang fails all of them."""
    env = {**os.environ, "PYTHONPATH": str(repo), "PYTHONDONTWRITEBYTECODE": "1"}
    try:
        done = subprocess.run([sys.executable, "-c", RUNNER, str(task / "hidden" / "checks.py")], cwd=repo, env=env,
                              text=True, capture_output=True, timeout=180, stdin=subprocess.DEVNULL)
        checks = json.loads(done.stdout.rsplit("@@RESULT@@", 1)[1])
    except (subprocess.TimeoutExpired, IndexError, ValueError):
        checks = {}
    sh(["git", "add", "-A", "-N"], repo)
    added = sum(int(line.split("\t")[0]) for line in sh(["git", "diff", "--numstat", meta["baseline_sha"], "--"], repo).stdout.splitlines() if line[0].isdigit())
    return {"checks": meta["checks"], "passed": sum(checks.values()),
            "missed": sorted(name for name, ok in checks.items() if not ok) or ([] if checks else ["all: checks could not run"]),
            "existing_tests_pass": sh(meta["regression"], repo).returncode == 0, "lines_added": added}


def validate(_):
    for task in sorted(p for p in TASKS.iterdir() if p.is_dir()):
        meta = load(task)
        if "solution" not in meta:
            print(f"{task.name}: open brief scored by rubric, no reference solution")
            continue
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            clone(task, repo, meta)
            before = score(repo, task, meta)
            for source, target in meta["solution"].items():
                shutil.copy(task / source, repo / target)
            after = score(repo, task, meta)
        print(f"{task.name}: baseline {before['passed']}/{meta['checks']}, reference {after['passed']}/{meta['checks']}")
        if before["passed"] or after["passed"] != meta["checks"]:
            raise SystemExit(f"task invalid: {after['missed']}")


def one(job, args):
    name, arm, rep = job
    task = TASKS / name
    meta = load(task)
    dest = args.out / name / arm / f"{rep:03d}"
    if (dest / "score.json").exists():
        return
    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True)
    work = Path(tempfile.mkdtemp(prefix="whittle-bench-"))
    repo = work / "repo"
    clone(task, repo, meta)
    text = arm_text(arm)
    if text:
        (work / "arm.md").write_text(text)
    argv = agent_command(args, work / "arm.md" if text else None)
    # Each turn is a new agent session on the same working tree: later turns see the code, not the earlier requests.
    started, status, stdout = time.time(), 0, ""
    for turn in meta["turns"]:
        try:
            agent = sh(argv + [(task / turn).read_text()], repo, timeout=args.timeout)
            status, stdout = status or agent.returncode, stdout + agent.stdout.rstrip("\n") + "\n"
        except subprocess.TimeoutExpired:
            status = "timeout"
            break
    result = {"task": name, "arm": arm, "run": f"{rep:03d}", **score(repo, task, meta),
              "agent": {"harness": args.harness, "model": args.model, **({"thinking": args.thinking} if args.harness == "pi" else {}),
                        "exit": status, "seconds": round(time.time() - started, 1), **usage(args.harness, stdout)}}
    (dest / "patch.diff").write_text(sh(["git", "diff", meta["baseline_sha"], "--"], repo).stdout)
    (dest / "transcript.jsonl").write_text(stdout)
    (dest / "score.json").write_text(json.dumps(result, indent=2) + "\n")
    shutil.rmtree(work, ignore_errors=True)
    print(f"{name} {arm} {rep:03d} {result['passed']}/{meta['checks']} ${result['agent']['tokens']['cost']:.4f} exit={status}", flush=True)


def run(args):
    args.out = args.out.resolve()
    for arm in args.arms:
        arm_text(arm)
    tasks = args.tasks or sorted(p.name for p in TASKS.iterdir() if p.is_dir())
    jobs = [(t, a, r) for t in tasks for a in args.arms for r in range(1, args.reps + 1)]
    random.Random(args.seed).shuffle(jobs)
    with ThreadPoolExecutor(args.jobs) as pool:
        list(pool.map(lambda job: one(job, args), jobs))
    sanitize(args.out)


def sanitize(runs: Path):
    """Replace the local username, home and temp paths in saved artifacts. Scores are not altered."""
    rules = [(re.compile(r"(?:/private)?/var/folders/[^/\s\"\\]+/[^/\s\"\\]+/T/"), "/tmp/"),
             (re.compile(re.escape(str(Path.home()))), "/home/user"), (re.compile(rf"\b{re.escape(getpass.getuser())}\b"), "user")]
    for path in runs.rglob("*"):
        if path.is_file() and path.suffix in {".json", ".jsonl", ".md", ".diff"}:
            text = clean = path.read_text(errors="replace")
            for pattern, replacement in rules:
                clean = pattern.sub(replacement, clean)
            if clean != text:
                path.write_text(clean)


def summarize(args):
    scores = [json.loads(p.read_text()) for p in sorted(args.runs.glob("*/*/*/score.json"))]
    agent = scores[0]["agent"]
    lines = [f"# {agent['harness']} · {agent['model']}", "",
             f"{len(scores)} runs. Delivered is the mean number of hidden checks passed; cost is list price as reported by the harness."]
    cells = {}
    for task in sorted({s["task"] for s in scores}):
        total = next(s["checks"] for s in scores if s["task"] == task)
        lines += ["", f"## {task}", "", f"| Arm | Runs | Delivered (of {total}) | Range | Output tokens | Cost | Seconds |", "|---|---|---|---|---|---|---|"]
        for arm in [a for a in ARMS if any(s["arm"] == a and s["task"] == task for s in scores)]:
            runs = [s for s in scores if s["arm"] == arm and s["task"] == task]
            passed = [s["passed"] for s in runs]
            mean = lambda pick, digits: round(statistics.mean(pick(s) for s in runs), digits)
            row = {"runs": len(runs), "delivered": round(statistics.mean(passed), 1), "min": min(passed), "max": max(passed),
                   "output_tokens": mean(lambda s: s["agent"]["tokens"]["output"], 0), "cost": mean(lambda s: s["agent"]["tokens"]["cost"], 4),
                   "seconds": mean(lambda s: s["agent"]["seconds"], 0)}
            cells[f"{task}/{arm}"] = row
            lines.append(f"| {arm} | {row['runs']} | {row['delivered']} | {row['min']}–{row['max']} | {row['output_tokens']:.0f} | ${row['cost']} | {row['seconds']:.0f} |")
        missed = {}
        for s in scores:
            if s["task"] == task:
                for name in s["missed"]:
                    missed.setdefault(name, {}).setdefault(s["arm"], 0)
                    missed[name][s["arm"]] += 1
        if missed:
            lines += ["", "Checks failed, as runs per arm:", ""]
            lines += [f"- `{name}`: " + ", ".join(f"{arm} {count}" for arm, count in sorted(arms.items())) for name, arms in sorted(missed.items())]
    (args.runs / "results.json").write_text(json.dumps({"agent": {k: agent[k] for k in ("harness", "model")}, "runs": len(scores), "cells": cells}, indent=2) + "\n")
    (args.runs / "results.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(required=True)
    sub.add_parser("validate", help="check every task: baseline passes nothing, reference passes everything").set_defaults(func=validate)
    r = sub.add_parser("run", help="run arms on tasks")
    r.add_argument("--harness", choices=["claude", "pi"], default="claude")
    r.add_argument("--model", required=True)
    r.add_argument("--thinking", default="medium", help="Pi only")
    r.add_argument("--reps", type=int, default=5)
    r.add_argument("--arms", nargs="*", default=["none", "ponytail", "whittle"])
    r.add_argument("--tasks", nargs="*")
    r.add_argument("--out", type=Path, required=True)
    r.add_argument("--jobs", type=int, default=4)
    r.add_argument("--timeout", type=int, default=1800)
    r.add_argument("--seed", type=int, default=20261005)
    r.set_defaults(func=run)
    s = sub.add_parser("summarize", help="write results.md and results.json for a runs directory")
    s.add_argument("runs", type=Path)
    s.set_defaults(func=summarize)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
