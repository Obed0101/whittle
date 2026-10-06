# Install

Whittle is one file of rules. Every route below puts the same three paragraphs where your agent reads them. Nothing else is installed.

| Agent | Command |
|---|---|
| Claude Code (plugin) | `/plugin marketplace add Obed0101/whittle` then `/plugin install whittle@whittle` |
| Claude Code (skill) | `mkdir -p ~/.claude/skills/whittle && curl -fsSL https://raw.githubusercontent.com/Obed0101/whittle/main/skills/whittle/SKILL.md -o ~/.claude/skills/whittle/SKILL.md` |
| Codex | `mkdir -p ~/.codex/skills/whittle && curl -fsSL https://raw.githubusercontent.com/Obed0101/whittle/main/skills/whittle/SKILL.md -o ~/.codex/skills/whittle/SKILL.md` |
| Pi | `mkdir -p ~/.pi/agent/skills/whittle && curl -fsSL https://raw.githubusercontent.com/Obed0101/whittle/main/skills/whittle/SKILL.md -o ~/.pi/agent/skills/whittle/SKILL.md` |
| Cursor | `mkdir -p .cursor/rules && curl -fsSL https://raw.githubusercontent.com/Obed0101/whittle/main/.cursor/rules/whittle.mdc -o .cursor/rules/whittle.mdc` |
| Windsurf | `mkdir -p .windsurf/rules && curl -fsSL https://raw.githubusercontent.com/Obed0101/whittle/main/.windsurf/rules/whittle.md -o .windsurf/rules/whittle.md` |
| Cline | `mkdir -p .clinerules && curl -fsSL https://raw.githubusercontent.com/Obed0101/whittle/main/.clinerules/whittle.md -o .clinerules/whittle.md` |
| Kiro | `mkdir -p .kiro/steering && curl -fsSL https://raw.githubusercontent.com/Obed0101/whittle/main/.kiro/steering/whittle.md -o .kiro/steering/whittle.md` |
| GitHub Copilot | `mkdir -p .github && curl -fsSL https://raw.githubusercontent.com/Obed0101/whittle/main/.github/copilot-instructions.md >> .github/copilot-instructions.md` |
| Gemini CLI | `curl -fsSL https://raw.githubusercontent.com/Obed0101/whittle/main/GEMINI.md >> GEMINI.md` |
| OpenCode, Amp, Zed, Jules and anything that reads `AGENTS.md` | `curl -fsSL https://raw.githubusercontent.com/Obed0101/whittle/main/AGENTS.md >> AGENTS.md` |

Or paste the three paragraphs from [`skills/whittle/SKILL.md`](skills/whittle/SKILL.md) into whatever rules file your agent has.

## What has been run

The published numbers come from Claude Code and Pi, with the skill text appended to the system prompt. The other rows place the same text at each tool's documented rules location and have not been benchmarked.

## Uninstall

Delete the file, or the three paragraphs.
