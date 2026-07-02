# Security Policy

## Reporting a vulnerability

If you find a security issue (secret leakage, unsafe code execution in the
task/agent sandbox, dependency vulnerability, etc.), please **do not** open
a public issue. Instead, use GitHub's [private vulnerability reporting](../../security/advisories/new)
for this repository, or email the maintainer directly.

Please include:

- A description of the vulnerability and its impact
- Steps to reproduce
- Affected version/commit

We aim to acknowledge reports within 5 business days.

## Scope notes specific to this project

- Task and agent code may execute SQL, PySpark, and Python. Contributed
  tasks and agents are reviewed before merge, but you should still treat
  `arena run` as executing untrusted code when running tasks you did not
  author yourself — use a container or VM if you're evaluating third-party
  submissions.
- Datasets in this repository must be synthetic (see
  [docs/dataset-policy.md](docs/dataset-policy.md)). Report any real or
  personally identifiable data you find as a security issue, not a bug.
- Never commit API keys, cloud credentials, or `.env` files. CI runs a
  secret scan on every PR, but treat that as a backstop, not a guarantee.
