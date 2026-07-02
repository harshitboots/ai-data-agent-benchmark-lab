# Changelog

All notable changes to this project are documented here, by date, matching
the daily-phase build log described in [ROADMAP.md](ROADMAP.md).

Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

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
