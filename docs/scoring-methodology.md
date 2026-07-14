# Scoring methodology

Every task defines its own scoring weights in `task.yaml`, validated by the
`ScoringWeights` model in [`arena/schema.py`](../arena/schema.py). There is
no single fixed split across all tasks — each task's author decides how much
each dimension matters for that task — but every task's five weights must
sum to exactly 100.

## The five dimensions

| Field | What it measures | Typically |
|---|---|---|
| `execution` | Did the agent's output run at all (SQL executes, PySpark job completes, dbt model builds)? | Deterministic |
| `correctness` | Does the output match `expected_output` (exact diff, unit tests, or a rule checklist)? | Deterministic |
| `efficiency` | Did the agent avoid wasteful execution (e.g. a full table scan where an index/partition prune was available)? | Deterministic where measurable, otherwise a rule checklist |
| `explanation` | Quality of the agent's reasoning or explanation of its own answer | LLM-judge — no deterministic check is possible here |
| `cost_latency` | Did the run stay within the task's `max_cost_usd` and finish in a reasonable time? | Deterministic, measured directly from the run |

This mirrors the project's core principle (see
[architecture.md](architecture.md#design-principles)): prefer a
deterministic check over an LLM-judge opinion wherever one exists. Of the
five dimensions, only `explanation` requires a judge; the other four are
computed directly from the run.

## Worked example — `retail_sql_001`

```yaml
scoring:
  execution: 30
  correctness: 40
  efficiency: 10
  explanation: 10
  cost_latency: 10
```

This task weights `correctness` highest (getting the repeat-customer logic
exactly right — date window, cancelled-order exclusion, test-customer
exclusion — is the point of the task) and `execution` second (the SQL has to
actually run against the provided CSVs). `explanation` and `efficiency` are
present but minor, since the task is small enough that query-plan efficiency
isn't the main thing being tested.

A task testing something like a full-table-scan anti-pattern would instead
weight `efficiency` heavily; a task about RAG citation quality would weight
`explanation` heavily. The schema doesn't prescribe a "correct" split — it
prescribes that every task author has to make the trade-off explicit and it
has to add up to 100.

## Final score

`arena run` / `arena score --run latest` compute this today (see
`evaluators/final_score.py`):

```text
final_score = Σ (dimension_weight / 100) × dimension_result
```

where each `dimension_result` is a 0–100 value produced by the evaluator for
that category (see [architecture.md](architecture.md) for how evaluators are
organized per task category). For `retail_sql_001` with the baseline agent,
that's currently `execution=100, correctness=100, efficiency=100,
explanation=0, cost_latency=100` → a final score of `90.0` (the baseline
agent never explains its answer, so it can't score above `100 -
explanation_weight` on any task).
