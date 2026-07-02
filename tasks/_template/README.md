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
| `evaluator.py` | Scores an agent's output against `expected/`. Interface lands in Phase 2 — see [ROADMAP.md](../../ROADMAP.md). |
| `metadata.json` | Free-form notes: dataset size, generation notes, reference dates used for any "trailing N months"-style logic. Keep any fixed reference dates here instead of using "today" — tasks must be reproducible regardless of when they're run. |

## Rules

- Data must be synthetic — no real, scraped, or company-private data. See
  [docs/dataset-policy.md](../../docs/dataset-policy.md).
- Keep the dataset as small as it can be while still exercising every rule
  in `success_criteria` — smaller datasets are faster to run in CI and
  easier for reviewers to hand-verify.
- No secrets or credentials anywhere in the task folder.
