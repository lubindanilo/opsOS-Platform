# OpsOS Platform — Project Context (Source of Truth)

## 0) Purpose (why this repo exists)
This repository is a **learning + portfolio** project designed to look and feel “production-like”.
Goal: build an end-to-end mini **Data + ML + LLM platform**, progressively, with real engineering standards.

Key idea: each phase must produce **concrete outputs** (CLI, tests, docs, benchmarks, deployable pieces),
not just theoretical notes.

## 1) Important constraint: the user is a beginner
The assistant must always:
1) State the **concrete objective**
2) Explain the concept **in simple terms**
3) Provide **copy/paste commands** step-by-step
4) Tell the **expected output**
5) Give a **minimal debug plan** (2–3 likely causes + commands)
6) Ask one quick comprehension question

No big leaps. No “do X then Y” without explanation.

## 2) Current stack
- OS: macOS (Apple Silicon)
- Python env/deps: **uv** + `.venv`
- Quality toolchain:
  - **ruff** (lint + format)
  - **mypy** (strict typing)
  - **pytest** (tests)
  - **pre-commit** (hooks)

## 3) Repository structure (current)
Top-level intent: monorepo style.
- `services/ingestor/` : Python package (ingestion component)
- `services/api/` : reserved for later (FastAPI)
- `tests/` : pytest tests
- `scripts/` : utility scripts (ex: perf dataset generator)
- `docs/` : documentation (perf notes, architecture, workflow)
- `data/` : **local outputs only** (must NOT be committed if large)

### 3.1 Critical repo hygiene
Never commit/push:
- `data/perf/` (big datasets + outputs)
- `data/out/` (generated outputs)
- `*.pstats` (profiling files)

Reason: GitHub rejects large files (100MB hard limit), and it pollutes the repo.
Only commit: code, scripts, docs, small examples.

## 4) Ingestor component (current architecture)
### 4.1 What it does
Input: CSV file with required columns:
- `event_id, ts, user_id, event_type, properties`

Process:
- parse CSV rows
- validate required fields
- parse timestamp (ISO, supports trailing `Z`)
- parse `properties` as JSON dict (via `json.loads`)
- produce canonical `Event` objects
- output: **JSONL** file (1 JSON per line)

### 4.2 Why JSONL
JSONL = “JSON Lines”: each line is a standalone JSON object.
It is good for streaming / incremental processing and easy debugging.

### 4.3 Main modules
- `services/ingestor/src/ingestor/models.py`
  - `Event` dataclass (frozen, slots)
- `services/ingestor/src/ingestor/csv_io.py`
  - `load_events_csv(path, strict=False, max_errors=50) -> (events, errors)`
  - `_parse_ts(...)`
  - `IngestError`
- `services/ingestor/src/ingestor/cli.py`
  - `main(...)` = CLI entrypoint
  - `_write_jsonl(...)` = JSONL writer

### 4.4 CLI usage
Command:
`uv run ingest --input <csv> --output <jsonl> [--strict] [--max-errors N] [--show-errors]`

Flags:
- `--strict` : stop at first invalid row (exit 1)
- `--max-errors` : cap collected errors in non-strict mode
- `--show-errors` : print all collected errors (otherwise first 5)

## 5) Quality workflow (must stay green)
Before any commit:
- `uv run ruff check --fix .`
- `uv run ruff format .`
- `uv run mypy .`
- `uv run pytest`

Goal: keep repo always shippable.

## 6) Performance / Profiling (Phase 1.6)
### 6.1 Dataset generation
Script:
- `scripts/gen_events_csv.py` generates `data/perf/events_1m.csv` (1,000,000 rows)

### 6.2 Benchmark commands
Realistic timing (honest):
- `time uv run ingest --input data/perf/events_1m.csv --output data/perf/out.jsonl --max-errors 1`

Profiling (slower due to overhead):
- `uv run python -m cProfile -o data/perf/profile.pstats -m ingestor.cli --input ... --output ...`
- `uv run python - <<'PY' ... pstats ... PY`

### 6.3 Key findings (what mattered)
- Baseline bottleneck was `dataclasses.asdict` causing massive `deepcopy`.
- Optimization #1: replaced `asdict(e)` with manual dict construction.
  Result: ~2.5x faster (example run: ~15.2s -> ~6.1s total on 1M rows).
- Optimization #2: compact JSON output via `json.dumps(..., separators=(",", ":"))`
  Result: small / noisy gain (may vary).

Current bottlenecks after opt #1:
- CSV iteration
- `json.loads` (properties)
- `json.dumps` (output)
- disk writes
- datetime parsing

## 7) “If something goes wrong” playbook
### 7.1 Push rejected due to large files
Symptoms: GitHub refuses push (GH001, file exceeds 100MB).
Fix approach:
1) Undo the commit (if not pushed): `git reset --soft HEAD~1`
2) Unstage big files: `git restore --staged data/perf data/out`
3) Add/verify `.gitignore` for `data/perf/`, `data/out/`, `*.pstats`
4) Remove cached tracking if needed: `git rm -r --cached data/perf`
5) Recommit only code/docs/scripts, push again.

### 7.2 Profiling shows only imports / tiny runtime
Cause: module not executing `main()` when run with `python -m`.
Fix: ensure `if __name__ == "__main__": raise SystemExit(main())` exists in `cli.py`.

## 8) Next technical steps (high level)
- Continue performance improvements based on profiler (not guessing).
- Start Phase 2 (SQL advanced) in parallel once Phase 1 docs are solid.
- Gradually add warehouse/dbt, orchestration, data quality, then cloud/docker/CI.
