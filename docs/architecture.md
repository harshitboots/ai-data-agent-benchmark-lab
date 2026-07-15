# Architecture

This document describes how a benchmark run flows through the system, which
directory owns which responsibility, and what's actually implemented today
versus what's still on the [ROADMAP](../ROADMAP.md).

## Pipeline

```text
Task Registry → Agent Runner → Tool Sandbox → Evaluators → Score Engine → Leaderboard
```

1. **Task Registry** — discovers and validates every `tasks/**/task.yaml`
   against the `TaskSpec` schema, and hands a task's description, input
   files, and success criteria to the runner.
2. **Agent Runner** — invokes the agent under test (baseline, OpenAI,
   Anthropic, a custom submission, ...) with the task prompt and input files,
   within the task's `time_limit_seconds` and `max_cost_usd` budget.
3. **Tool Sandbox** — the connector layer the agent's code actually executes
   against (DuckDB for SQL tasks, a PySpark session, a mock warehouse
   connector, a PDF reader, ...), isolated per run.
4. **Evaluators** — deterministic-first checks per category: does the SQL
   run, does the output diff-match `expected_output`, do PySpark unit tests
   pass, does the dbt model build. LLM-judge evaluation is used only where no
   deterministic check is possible (e.g. explanation quality).
5. **Score Engine** — combines evaluator results into the weighted score
   defined by each task's `scoring:` block — see
   [scoring-methodology.md](scoring-methodology.md).
6. **Leaderboard** — aggregates scored runs across agents/tasks into
   `leaderboard/results.json` and a rendered `leaderboard.md`.

## Directory → component map

| Directory | Component | Status |
|---|---|---|
| [`tasks/`](../tasks/) | Task Registry (data) | Live — one real task (`sql_analytics/retail_sql_001`), rest are category placeholders |
| [`arena/`](../arena/) | Task Registry, Agent Runner, Score Engine (code) + CLI | Live — `task_loader.py`, `schema.py`, `agent.py`, `runner.py`, `scoring.py`, `cli.py` (`list-tasks`, `show-task`, `validate-tasks`, `run`, `score`, `version`) |
| [`agents/`](../agents/) | Agent Runner (implementations) | Live for `sql_analytics` — `baseline_agent/` (deterministic); `custom_agent_template/` defines the `BaseAgent` contract other agents implement against |
| [`connectors/`](../connectors/) | Tool Sandbox | Live: `duckdb/`. Stubs: `sqlite/`, `csv/`, `parquet/`, `postgres/`, mock warehouse connectors |
| [`evaluators/`](../evaluators/) | Evaluators | Live: `sql_evaluator.py`, `final_score.py`. Stubs for other task categories |
| [`leaderboard/`](../leaderboard/) | Leaderboard | Live — `leaderboard_generator.py`, `results.json`, `leaderboard.md`, `submissions/` |
| [`datasets/`](../datasets/) | Synthetic data backing tasks | Stubs — see [dataset-policy.md](dataset-policy.md) |

`arena run --task retail_sql_001 --agent baseline`, `arena score --run
latest`, `arena run ... --submit` and `arena leaderboard` all work end to
end today. The pipeline above is fully wired for the `sql_analytics`
category; other categories (PySpark, dbt, RAG, ...) need their own
connector/evaluator before `arena run` supports them — see
[ROADMAP.md](../ROADMAP.md) for what's next.

## Design principles

- **Deterministic checks over LLM-judge opinions wherever possible.** A SQL
  query either executes and matches `expected_output.csv`, or it doesn't —
  that's not a judgment call.
- **No real or scraped data, anywhere.** Every dataset is synthetic; see
  [dataset-policy.md](dataset-policy.md).
- **Agent code runs as untrusted input.** Contributed agents and tasks
  execute SQL/PySpark/Python; see [SECURITY.md](../SECURITY.md) for the
  sandboxing expectations this places on `arena run`.
- **Every task is self-contained.** A task folder ships its own input data,
  expected output, and success criteria — no shared fixtures, so a task can
  be understood and graded in isolation.
