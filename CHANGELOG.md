# Changelog

All notable changes to this project are documented here, by date, matching
the daily-phase build log described in [ROADMAP.md](ROADMAP.md).

Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## 2026-07-15 — Phase 3: leaderboard

### Added
- `leaderboard/leaderboard_generator.py` — aggregates
  `leaderboard/submissions/*.json` into `leaderboard/results.json` and a
  rendered `leaderboard/leaderboard.md`, ranked per task by `final_score`,
  deduped to the newest submission per (task, agent, submitter); runnable
  standalone via `python -m leaderboard.leaderboard_generator`
- `arena/leaderboard.py`, `arena leaderboard` command (optional `--task`
  filter) — regenerates and renders the leaderboard as a table
- `arena run --submit [--submitted-by NAME]` — publishes a run into
  `leaderboard/submissions/` (defaults `--submitted-by` to `git config
  user.name`, falling back to `"anonymous"`); reuses the existing
  `RunResult` shape, no new schema
- `leaderboard/submissions/retail_sql_001__baseline__harshitboots.json` —
  seeded with a real `arena run --submit` result, not a hand-written fixture
- `.github/workflows/update-leaderboard.yml` — verifies (doesn't
  auto-commit) that `leaderboard/results.json`/`leaderboard.md` match what
  the generator produces from `leaderboard/submissions/`; auto-committing
  would hit the same PR-required branch protection on `main` that everyone
  else is subject to
- `leaderboard*` is now a real installed package (`pyproject.toml`)
- `tests/test_leaderboard.py` (5 new tests, 18 total passing)

## 2026-07-14 — Phase 2: evaluation engine

### Added
- `connectors/duckdb/` — loads task input CSVs into an in-memory DuckDB
  connection (via DuckDB's own CSV reader, so dates/types infer correctly)
  and runs SQL against them
- `evaluators/sql_evaluator.py` — scores execution, correctness (exact diff
  against `expected_output`), efficiency, explanation, and cost/latency for
  a `sql_analytics` run; `evaluators/final_score.py` combines them using the
  task's own weighted `scoring:` block
- `agents/baseline_agent/` — deterministic, no-LLM agent implementing the
  new `arena.agent.BaseAgent` interface; looks up a checked-in solution
  under `solutions/<task_id>.sql`
- `agents/custom_agent_template/template_agent.py` — the actual
  `BaseAgent` skeleton contributors copy, referenced by `CONTRIBUTING.md`
- `arena/runner.py`, `arena/scoring.py` — orchestrates agent → evaluator →
  final score, and saves/loads run results under `runs/`
- `arena run --task <id> --agent <name>` and `arena score --run latest` —
  both work end-to-end against `retail_sql_001`
- `agents/`, `connectors/`, `evaluators/` are now real installed packages
  (`pyproject.toml`'s `packages.find.include`), not CWD-dependent imports
- `tests/test_duckdb_connector.py`, `tests/test_sql_evaluator.py`,
  `tests/test_runner.py` (9 new tests, 13 total passing)

### Fixed
- README's illustrative quick-start "Expected output" block (£ currency,
  a "Hallucination Risk" field) never matched the real 5-dimension
  `ScoringWeights` schema — replaced with actual `arena run` output

## 2026-07-03 — Phase 1: task schema & CLI skeleton

### Added
- `arena/schema.py` — `TaskSpec`/`ScoringWeights` Pydantic models
- `arena/config.py`, `arena/task_loader.py` — task discovery/loading
- `arena/cli.py` (Typer) — `arena list-tasks`, `arena show-task` (both
  installed and verified working via `pip install -e .`)
- First real task: `tasks/sql_analytics/retail_sql_001/` — synthetic,
  hand-verified retail dataset and expected output
- `tasks/_template/` — documented task schema template for contributors
  (moved up from Phase 4 since the schema now exists)
- `tests/test_task_loader.py` (4 tests, passing)
- Branch protection enabled on `main`: PR + 1 approval required for
  non-admins, no force-push/delete

## 2026-07-02 — Phase 0: Foundation

### Added
- Full repository directory scaffold (`arena/`, `agents/`, `tasks/`,
  `datasets/`, `evaluators/`, `connectors/`, `leaderboard/`, `docs/`,
  `examples/`, `tests/`, `.github/`, `assets/`) with per-folder README
  stubs describing what lands in each phase
- `README.md`, `LICENSE` (Apache 2.0), `CONTRIBUTING.md`,
  `CODE_OF_CONDUCT.md`, `SECURITY.md`, `ROADMAP.md`, `CITATION.cff`
- `pyproject.toml`, `requirements.txt`, `.gitignore`, `Makefile`
- GitHub repository created under `harshitboots/ai-data-agent-benchmark-lab`
