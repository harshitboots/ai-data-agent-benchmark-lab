# Contributing

Thanks for considering a contribution. This project is built in daily,
public phases (see [ROADMAP.md](ROADMAP.md)) — check there first so your PR
lands on top of the current phase instead of a future one.

## Local setup

```bash
git clone https://github.com/harshitboots/ai-data-agent-benchmark-lab.git
cd ai-data-agent-benchmark-lab
pip install -e ".[dev]"
pytest
```

## Ways to contribute

| Path | Where to start |
|---|---|
| Add a benchmark task | Copy [tasks/_template/](tasks/_template/), fill in `task.yaml`, input data, expected output, and an evaluator |
| Add a dataset | Add a synthetic dataset under [datasets/](datasets/) with a data dictionary and generation script — no real or scraped data |
| Add an agent | Copy [agents/custom_agent_template/](agents/custom_agent_template/) and implement the `BaseAgent` interface |
| Add/improve an evaluator | See [evaluators/](evaluators/) — deterministic checks first, LLM-judge only where no deterministic check is possible |
| Improve docs | See [docs/](docs/) |
| Submit a leaderboard result | See [leaderboard/submissions/](leaderboard/submissions/) |

## Adding a task — checklist

- [ ] `task.yaml` follows the schema in `tasks/_template/task.yaml`
- [ ] Input data is synthetic (see [docs/dataset-policy.md](docs/dataset-policy.md))
- [ ] No secrets, credentials, or PII anywhere in the task folder
- [ ] `evaluator.py` runs standalone and returns a score breakdown
- [ ] The baseline agent can run against the task (even if it scores low)
- [ ] `README.md` explains the task in plain language

## Branch protection

`main` is protected: nobody can push directly to it, and every pull request
needs at least **1 approving review** before it can be merged. Stale
approvals are dismissed automatically when new commits are pushed, and
force-pushes/deletion of `main` are disabled. (The repo owner can bypass
this for solo maintenance work, but the expectation for everyone else,
including new maintainers, is PR + review, no exceptions.)

## Pull request review

Every PR is checked (locally and in CI) for:

1. Tests pass
2. Task/agent schema validates
3. No secrets or PII patterns
4. No large binary files
5. Docs build

## Commit style

Small, focused commits. Prefer `feat:`, `fix:`, `docs:`, `task:`, `agent:`,
`evaluator:` prefixes so the history stays scannable.

## Code of conduct

By participating, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).
