# evaluators

Deterministic + LLM-judge evaluators, one per task category.

- [`sql_evaluator.py`](sql_evaluator.py) — scores a `sql_analytics` agent
  run's `execution`, `correctness` (exact diff against `expected_output`),
  `efficiency`, `explanation`, and `cost_latency` dimensions.
- [`final_score.py`](final_score.py) — combines those five `DimensionResult`s
  into a single 0-100 score using the task's own `scoring:` weights. See
  [docs/scoring-methodology.md](../docs/scoring-methodology.md).

More evaluators (PySpark, dbt, RAG, PII, data quality, ...) land as those
task categories get built — see [ROADMAP.md](../ROADMAP.md).

