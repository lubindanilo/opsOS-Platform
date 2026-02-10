# OpsOS Platform — Workflow (How we work)

## Golden rule
Never optimize or refactor “by feel”.
Always: measure → identify bottleneck → change → measure again → document.

## Before any commit (quality gate)
Run:
- `uv run ruff check --fix .`
- `uv run ruff format .`
- `uv run mypy .`
- `uv run pytest`

## Git discipline (solo but professional)
- one feature per commit
- clear commit message
- avoid committing generated data (data/perf, data/out, *.pstats)

## Debug template
When something fails:
1) copy error
2) identify file/line
3) explain root cause
4) apply minimal fix
5) verify with tests + rerun command
