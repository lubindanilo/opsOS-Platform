# Repo rules (must-read)

## Never commit large generated files
Do NOT commit/push:
- `data/perf/`
- `data/out/`
- `*.pstats`
- `.venv/`

Reason: GitHub rejects large files (>100MB) and it pollutes the repo.

## Quality gate before commit
Run:
- `uv run ruff check --fix .`
- `uv run ruff format .`
- `uv run mypy .`
- `uv run pytest`
