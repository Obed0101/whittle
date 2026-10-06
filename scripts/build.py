#!/usr/bin/env python3
"""Generate every agent's rules file from skills/whittle/SKILL.md, the single source.

  python3 scripts/build.py          write the files
  python3 scripts/build.py --check  exit 1 if any file is out of date (used in CI)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION = "1.0.0"
DESCRIPTION = "Cut the code, not the product. Ship everything that was asked for; spend nothing on the rest."

skill = (ROOT / "skills" / "whittle" / "SKILL.md").read_text()
rules = skill.split("---", 2)[2].strip() + "\n"


def front(**fields):
    return "---\n" + "".join(f"{key}: {value}\n" for key, value in fields.items()) + "---\n\n"


FILES = {
    # Codex, OpenCode, Pi, Amp, Zed, Jules and every agent that reads AGENTS.md.
    "AGENTS.md": rules,
    "GEMINI.md": rules,
    ".cursor/rules/whittle.mdc": front(description=DESCRIPTION, alwaysApply="true") + rules,
    ".windsurf/rules/whittle.md": front(trigger="always_on") + rules,
    ".clinerules/whittle.md": rules,
    ".kiro/steering/whittle.md": front(inclusion="always") + rules,
    ".github/copilot-instructions.md": rules,
    ".claude-plugin/plugin.json": json.dumps({"name": "whittle", "version": VERSION, "description": DESCRIPTION,
                                              "author": {"name": "Obed0101"}, "repository": "https://github.com/Obed0101/whittle",
                                              "license": "MIT"}, indent=2) + "\n",
    ".claude-plugin/marketplace.json": json.dumps({"name": "whittle", "owner": {"name": "Obed0101"},
                                                   "plugins": [{"name": "whittle", "source": "./", "description": DESCRIPTION}]}, indent=2) + "\n",
}

stale = []
for name, content in FILES.items():
    path = ROOT / name
    if "--check" in sys.argv:
        if not path.exists() or path.read_text() != content:
            stale.append(name)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
if stale:
    sys.exit("out of date, run scripts/build.py: " + ", ".join(stale))
print(f"{len(FILES)} files {'in sync' if '--check' in sys.argv else 'written'}")
