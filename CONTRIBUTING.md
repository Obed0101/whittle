# Contributing

Whittle is three paragraphs and a benchmark. Both stay small on purpose.

## Changing the skill

A change to `skills/whittle/SKILL.md` needs runs, not arguments. Open the pull request with:

1. The edited skill, and `python3 scripts/build.py` run so every agent file matches it.
2. A runs directory from `bench/bench.py` for the arms `none`, `ponytail` and `whittle` on the two open briefs (`kanban`, `notes`), at least 5 runs per cell, same model for every arm.
3. The generated `results.md`, unedited.

A wording change that does not move the numbers will be closed. So will one that moves them only on the task it was tuned on: say which task you iterated against and which you held out.

## Adding a task or an arm

- A task is a folder in `bench/tasks/` with a frozen `baseline.bundle`, the request, and `hidden/checks.py` with one test per thing asked. `python3 bench/bench.py validate` must show the baseline passing nothing and the reference passing everything.
- An arm is an entry in `bench/arms.json`. Other people's skills are pinned by git blob SHA and fetched at run time; do not copy them into this repository.

## Reporting a result that disagrees

Welcome, especially those. Open an issue with the runs directory. Numbers without the patches and transcripts behind them are not accepted in either direction.

## What will not be merged

Hooks, modes, personas, a longer skill, generated prose, or a results table that does not regenerate from the committed `score.json` files.
