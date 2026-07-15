# submissions

Community-submitted benchmark results, one file per (task, agent, submitter).

## How to submit a result

```bash
arena run --task retail_sql_001 --agent baseline --submit --submitted-by your-github-handle
```

This writes `<task_id>__<agent_name>__<submitted_by>.json` here — the same
shape `arena run` already writes to the (gitignored, local-only) `runs/`
directory, plus a `submitted_by` field. Resubmitting under the same
task/agent/name overwrites your previous submission.

Then regenerate the public leaderboard and commit both the new submission
file and the regenerated artifacts:

```bash
arena leaderboard
git add leaderboard/
git commit -m "leaderboard: submit <agent> on <task>"
```

`.github/workflows/update-leaderboard.yml` will fail your PR if
`leaderboard/results.json`/`leaderboard.md` don't match what
`leaderboard_generator.py` produces from the submissions in this folder —
run `arena leaderboard` locally before opening the PR.

See [ROADMAP.md](../../ROADMAP.md) for the phase plan.
