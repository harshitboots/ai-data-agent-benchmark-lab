# Dataset policy

## The rule

Every dataset in this repository must be **synthetic**. No real customer
data, no scraped data, no data derived from a real company's actual records,
no real personally identifiable information (PII) — ever, including in
example rows, fixtures, or task templates.

This isn't just a licensing precaution: PII-detection and data-quality tasks
specifically ask an agent to find fake emails, fake card-like numbers, and
fake broken records. Using real data for that would defeat the purpose (an
agent could "cheat" by pattern-matching real-looking data sources) and would
expose this project and its contributors to real privacy/legal risk for no
benefit.

If you find real or scraped data anywhere in this repository, report it as a
**security issue** (see [SECURITY.md](../SECURITY.md)), not a regular bug —
it will be treated with the same urgency as a credential leak.

## What "synthetic" means here

- Generated programmatically (a Python/Faker script, hand-crafted rows, or
  similar) — not exported or copy-pasted from any real system.
- Internally consistent but fictional: fake company names, fake customer
  IDs, fake products. Realistic in shape, fictional in substance.
- Small and deterministic where possible. `tasks/sql_analytics/retail_sql_001`
  is the reference example: 8 customers, 8 products, 19 orders — hand-crafted
  specifically so the expected output can be verified by a human and the
  whole task runs fast in CI (see its `metadata.json`).
- Free of any real names, addresses, emails, phone numbers, or account
  numbers, even as "flavor" — use obviously fake values
  (`jane.doe@example.com`, `555-0100`-style numbers) so nobody can mistake a
  fixture for a leak.

## Where datasets live

- [`datasets/`](../datasets/) — larger, reusable synthetic datasets shared
  across multiple tasks in a domain (`retail`, `ecommerce`, `finance_synthetic`,
  `healthcare_synthetic`, `telecom`, `logistics`, `education`).
- `tasks/<category>/<task_id>/input/` — data scoped to a single task, used
  when a dataset doesn't need to be shared.

Domain folders under `datasets/` that use a `_synthetic` suffix
(`finance_synthetic`, `healthcare_synthetic`) are named that way deliberately
— those domains are the ones where mistaking a fixture for real data would be
most damaging (health records, financial records), so the suffix is a
standing reminder at the folder level, not just in this doc.

## Adding a new dataset or task

Per [CONTRIBUTING.md](../CONTRIBUTING.md)'s task checklist:

1. Generate the data yourself (script or hand-crafted) — don't import
   anything from an external source, including "anonymized" real data.
2. If it's a shared dataset under `datasets/<domain>/`, include a data
   dictionary describing each column, and ideally the generation script
   itself so the dataset is reproducible.
3. Keep row counts as small as the task allows — large synthetic datasets
   slow down CI and make hand-verifying `expected_output` harder.
4. Double-check there's no accidental PII before opening a PR — copy-pasting
   a "realistic-looking" example from documentation, Stack Overflow, or an
   LLM's own training data can sometimes reproduce a real record. When in
   doubt, regenerate the field rather than trust it.

## Licensing

Datasets in this repository are original synthetic work released under the
same [Apache 2.0](../LICENSE) license as the rest of the project, unless a
specific dataset's own README states otherwise.
