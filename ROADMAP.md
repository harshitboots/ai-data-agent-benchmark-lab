# Roadmap

This project is being built in daily phases, in the open. Each phase ends in a
commit and a push, so progress is always visible in the commit history. This
file is the single source of truth for "what's done" and "what's next" —
update the checkboxes as phases land instead of trusting memory or chat logs.

## Phase 0 — Foundation (Day 1)
- [x] Repository scaffold: full directory layout for `arena/`, `agents/`,
      `tasks/`, `datasets/`, `evaluators/`, `connectors/`, `leaderboard/`,
      `docs/`, `examples/`, `tests/`, `.github/`, `assets/`
- [x] README, LICENSE (Apache 2.0), CONTRIBUTING, CODE_OF_CONDUCT, SECURITY,
      CHANGELOG, CITATION.cff
- [x] `pyproject.toml`, `requirements.txt`, `.gitignore`, `Makefile`
- [x] GitHub repository created and Phase 0 pushed

## Phase 1 — Task schema & CLI skeleton (Day 2–3)
- [x] `task.yaml` schema (Pydantic models) shared by every task
- [x] `arena/task_loader.py`, `arena/config.py`
- [x] `arena/cli.py` (Typer) with `arena list-tasks` and `arena show-task`
- [x] First real task: `tasks/sql_analytics/retail_sql_001/` with synthetic
      retail dataset (customers, orders, products), hand-verified expected
      output
- [x] `tasks/_template/` (moved up from Phase 4 — needed as soon as the
      schema exists so contributors aren't blocked)
- [x] `tests/test_task_loader.py`

## Phase 2 — Evaluation engine (Day 4–5)
- [ ] `connectors/duckdb/` connector
- [ ] `evaluators/sql_evaluator.py`, `evaluators/final_score.py`
- [ ] `arena/runner.py`, `arena/scoring.py`
- [ ] `agents/baseline_agent/` (deterministic, no LLM dependency)
- [ ] `arena run --task retail_sql_001 --agent baseline` works end-to-end
- [ ] `arena score --run latest` works end-to-end

## Phase 3 — Leaderboard (Day 6)
- [ ] `arena/leaderboard.py`, `leaderboard/leaderboard_generator.py`
- [ ] `leaderboard/results.json`, `leaderboard/leaderboard.md`
- [ ] `arena leaderboard` command
- [ ] `.github/workflows/update-leaderboard.yml`

## Phase 4 — More task categories (Day 7–8)
- [ ] PySpark task + `pyspark_evaluator.py`
- [ ] PII detection task + `pii_evaluator.py`
- [ ] Data quality task + `data_quality_evaluator.py`

## Phase 5 — Agent templates (Day 9)
- [ ] `agents/openai_agent/`, `agents/anthropic_agent/`
- [ ] `agents/langchain_agent/`
- [ ] `agents/custom_agent_template/` with docs for contributors

## Phase 6 — Contribution infrastructure (Day 10)
- [ ] Issue templates, PR template, labels
- [ ] `.github/workflows/test.yml`, `validate-task.yml`, `secret-scan.yml`
- [ ] `tests/` covering task loader, runner, scoring, sql evaluator

## Phase 7 — Docs site (Day 11)
- [ ] MkDocs setup, `docs/` content, architecture diagram
- [ ] Publish to GitHub Pages

## Phase 8 — Breadth & launch (Day 12+)
- [ ] RAG task, pipeline-debugging task, cost-optimisation task
- [ ] Learning mode (`arena learn`), enterprise/private mode
- [ ] Good-first-issues, launch post

Status key: unchecked = not started, checked = merged to `main`.
