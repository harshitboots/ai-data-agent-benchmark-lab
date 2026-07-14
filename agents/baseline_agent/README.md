# baseline_agent

Deterministic, no-LLM baseline agent used as the scoring floor for every
task. Implements `arena.agent.BaseAgent` — see [`__init__.py`](__init__.py).
It looks up a known-correct solution under [`solutions/`](solutions/) by
task ID (currently just `retail_sql_001.sql`) and returns it as-is; tasks
without a checked-in solution fail cleanly instead of crashing the run.

Try it: `arena run --task retail_sql_001 --agent baseline`

See [ROADMAP.md](../../ROADMAP.md) for the phase plan.

