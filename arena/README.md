# arena

Core engine: CLI, task loader, runner, scoring, leaderboard, telemetry.

| Module | Status |
|---|---|
| `config.py` | done — path constants |
| `schema.py` | done — `TaskSpec` / `ScoringWeights` Pydantic models |
| `task_loader.py` | done — discover and load `task.yaml` files |
| `cli.py` | done — `arena list-tasks`, `arena show-task` |
| `runner.py`, `scoring.py` | Phase 2 |
| `leaderboard.py`, `telemetry.py`, `utils.py` | Phase 3+ |

See [ROADMAP.md](../ROADMAP.md) for the phase plan.

