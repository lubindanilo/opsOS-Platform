# OpsOS Platform — Roadmap (Multi-month)

## Phase 0 — Setup Engineer (done)
- GitHub SSH OK, repo clean, uv installed
- ruff/mypy/pytest/pre-commit configured
- baseline monorepo structure

DoD:
- `uv run ruff/mypy/pytest` all green
- first commit pushed

## Phase 1 — Python intermediate (in progress)
- typed code (mypy strict)
- packaging + CLI
- tests
- perf/profiling + docs

DoD:
- stable ingestor package + CLI
- tests cover strict/non-strict + limits
- `docs/perf.md` with baseline/opt results

## Phase 2 — SQL advanced
- window functions
- modeling (star schema)
- performance (EXPLAIN ANALYZE, indexes)
Output:
- `warehouse/` or `sql/` folder with 10+ real queries + optimization proof

## Phase 3 — CS fundamentals
- DS/Algo/Complexity (30–40 quality problems + write-ups)
- OS basics
- Networking basics
Output:
- `docs/cs-notes/` + solved set + reasoning

## Phase 4 — Git + Code Review + Architecture
- PR discipline, clean history
- conventions, boundaries, retries/idempotence
Output:
- `docs/architecture.md` + conventions

## Phase 5 — Data Engineering
- orchestration (Dagster or Airflow)
- dbt transformations
- data quality (Great Expectations)
- (concept) Spark + Kafka
Output:
- orchestrated pipeline: ingest → validate → transform → publish

## Phase 6 — Cloud + Docker + CI/CD
- AWS fundamentals (IAM, VPC, S3, compute, RDS, logs/alarms)
- docker-compose local system
- GitHub Actions CI pipeline
Output:
- `docker-compose up` runs the stack
- CI green on push

## Phase 7 — MLOps
- MLflow/W&B tracking, model registry
- drift monitoring
- (concept) feature store
Output:
- /predict endpoint + model versioning + monitoring job

## Phase 8 — LLM Engineering
- RAG (chunking, retrieval)
- evaluation dataset + metrics
- guardrails
- latency/cost optimization
Output:
- /ask endpoint + eval scores + guardrails
