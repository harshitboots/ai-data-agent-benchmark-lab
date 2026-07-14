# Task template

Copy this entire folder to `tasks/<category>/<task_id>/` to create a new
benchmark task. See [CONTRIBUTING.md](../../CONTRIBUTING.md) for the full
contribution checklist. Reference implementation to copy the shape of:
[tasks/sql_analytics/retail_sql_001/](../sql_analytics/retail_sql_001/).

## Folder contents

| File/folder | Purpose |
|---|---|
| `task.yaml` | Machine-readable task spec — parsed by `arena.task_loader` into a `TaskSpec`. Every field is documented inline in the template. |
| `README.md` | Plain-language explanation of the task for humans (replace this file's contents with your task's own README). |
| `input/` | The files the agent is given, listed in `task.yaml`'s `input_files`. |
| `expected/` | The expected output, named to match `task.yaml`'s `expected_output`. |
| `metadata.json` | Free-form notes: dataset size, generation notes, reference dates used for any "trailing N months"-style logic. Keep any fixed reference dates here instead of using "today" — tasks must be reproducible regardless of when they're run. |

There's no per-task `evaluator.py` — scoring is done by a shared evaluator
per task **category** (e.g. every `sql_analytics` task is scored by
[`evaluators/sql_evaluator.py`](../../evaluators/sql_evaluator.py), which
diffs the agent's output against `expected/expected_output.csv`). If your
task's category doesn't have an evaluator yet, it can't be run/scored until
one is added — see [docs/architecture.md](../../docs/architecture.md).

## Rules

- Data must be synthetic — no real, scraped, or company-private data. See
  [docs/dataset-policy.md](../../docs/dataset-policy.md).
- Keep the dataset as small as it can be while still exercising every rule
  in `success_criteria` — smaller datasets are faster to run in CI and
  easier for reviewers to hand-verify.
- No secrets or credentials anywhere in the task folder.
