<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/whittle-logo-horizontal-white.svg">
    <img src="assets/whittle-logo-horizontal-black.svg" width="300" alt="Whittle">
  </picture>
</p>

<p align="center"><strong>Cut the code, not the product.</strong></p>

<p align="center">A 171-word skill for coding agents: ship everything you asked for, spend nothing on the rest.</p>

<p align="center"><a href="https://whittle-skill.vercel.app">whittle-skill.vercel.app</a></p>

---

Minimal-code skills report how little got written. Nobody reports what got left out.

So we measured it. Same model, same two-sentence brief, and a hidden checklist of what a finished product has:

> Build a personal kanban board as a web app. I want a complete product I could use every day, not a demo.

| Claude Sonnet 5.5 · two apps from scratch · 5 runs each | Product delivered | Cost per run |
|---|--:|--:|
| No skill | 91–94% | $0.30–0.46 |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | 82–83% | $0.19–0.20 |
| **Whittle** | **94–95%** | **$0.26–0.27** |

Ranges span two rounds: October 5 against Ponytail before v5, and October 14 against Ponytail 5.2.0.

Ponytail is the cheapest because it ships less. Its own skill says a vague request "gets the smallest version that does the core job". A cheap run that leaves out what you asked for is not a saving: you pay for the missing part later, by hand or in another run.

Whittle ships the whole product and costs about 30% less than no skill on average, 11–41% depending on the round. Not on every task: on the October 14 kanban runs it cost slightly more than no skill ($0.30 against $0.26), and all of that round's saving came from notes.

Which features got built on the kanban board against Ponytail 5, in runs out of 5. These are the six that Ponytail 5 left out of most of its boards:

| Built in | No skill | Ponytail 5 | Whittle |
|---|:-:|:-:|:-:|
| Archive or trash | 5/5 | 0/5 | 5/5 |
| Checklists or subtasks | 5/5 | 0/5 | 5/5 |
| Work-in-progress limits | 5/5 | 1/5 | 3/5 |
| Reordering columns | 3/5 | 2/5 | 2/5 |
| Versioned saved data | 1/5 | 0/5 | 5/5 |
| Motion that respects reduced motion | 0/5 | 0/5 | 5/5 |

Every run, patch and score: [October 5](bench/runs/claude-sonnet-5-5/results.md), [October 14](bench/runs/claude-sonnet-5-5-ponytail-5/results.md).

## The whole skill

```markdown
Deliver the whole outcome that was asked for, at the level of polish it was asked for. Never shrink
the request, ship a reduced version, or stop at a demo. An open request ("complete", "polished",
"something I can use every day") is scope: a finished product has every core flow and the features
regular users of the best tools of its kind rely on, editing and deleting, undo and recovery, ways to
organize and find things, keyboard and screen-reader use, phone layout, dark mode, reduced motion,
empty and error states, and keeps the user's data safe, portable and versioned so a later release can
still read it.

Spend nothing on anything else. No abstraction with one user, no developer-facing option or config
nobody asked for, no wrapper, no speculative extension point, no dependency for a few lines, no
duplicated logic, no comment that restates the code, no plan, no narration. Look once, write each
file once, verify once.

Final message: what was built and what was not verified, in three sentences.
```

That is all of it. No hooks, no modes, no persona. 171 words against 1,079 in the skill file it is compared with, and a ruleset is reread on every call your agent makes.

## Install

Claude Code:

```
/plugin marketplace add Obed0101/whittle
/plugin install whittle@whittle
```

Claude loads a plugin skill when it judges the task fits. In a clean install it did on 4 of 5 ordinary requests and skipped a small CLI script. The benchmark appends the skill to the system prompt instead; to get that, paste the three paragraphs into `CLAUDE.md`.

Codex, Pi, Cursor, Windsurf, Cline, Kiro, Copilot, Gemini CLI and anything that reads `AGENTS.md`: one line each in [INSTALL.md](INSTALL.md). Or paste the three paragraphs into your agent's rules file.

## What we do not claim

- **Whittle is not cheaper than Ponytail.** It costs about a third more per run. The claim is that it does not pay for its saving with your product.
- **On GPT the effect is much smaller.** With GPT-6 Luna in Pi, 10 runs per cell, the four tasks that come with an explicit spec turn out the same for no skill, Ponytail, Caveman and Whittle, in delivery and in cost. On the open kanban brief Whittle delivers 30.0–31.2 of 40 against 27.2–27.6 with no skill and 26.3–26.7 with Ponytail, at the lowest cost of the three in both rounds. In the October 14 round two Whittle runs on spec tasks shipped a CLI that crashes on start (a custom `--help` that collides with argparse's), which no other arm did; they count as delivered nothing. Numbers: [October 5](bench/runs/pi-gpt-6-luna/results.md), [October 14](bench/runs/pi-gpt-6-luna-ponytail-5/results.md).
- **The checklist sees what was built, not how well it works.** On the open briefs each check is a pattern search over the delivered HTML, CSS and JavaScript. Read the score as breadth.
- **Small sample.** Two rounds of five runs per cell, one Claude model, two briefs. On kanban the Ponytail gap does not overlap with the other arms in either round; on notes it does in the October 14 round. The difference between Whittle and no skill is inside the noise, and the cost of no skill moved by a third between rounds while nothing in the benchmark changed.
- **Three known biases, all in Whittle's favor.** The kanban checklist was extended after seeing what the model builds unprompted. The skill names categories (keyboard, dark mode, reduced motion, versioned data) that the checklists also look for. And the skill was revised once after its first scores on both briefs, then run again; the numbers above are that second version, so no brief here is unseen by it. The notes checklist itself was written before any output existed.
- **Ponytail was tested as its skill file**, pinned by blob SHA in [`bench/arms.json`](bench/arms.json) (`02c0712` on October 5, `b76922f` from v5.2.0 on October 14) and appended to the system prompt, not as the full plugin with hooks.

## Run it yourself

```bash
cd bench
python3 bench.py validate
python3 bench.py run --harness claude --model claude-sonnet-5-5 --tasks kanban notes --out runs/mine
python3 bench.py summarize runs/mine
```

Each run starts from a frozen git bundle in a temporary directory with no user settings, skills or MCP servers loaded, and is scored by checks the agent never saw. Add your own skill as an arm in `arms.json`. More in [bench/README.md](bench/README.md).

If your numbers disagree with ours, open an issue with the runs directory. [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Code and skill: [MIT](LICENSE). The Whittle name and logo are not covered by that license. Ponytail and Caveman are fetched at run time from their own repositories and are not redistributed here.
