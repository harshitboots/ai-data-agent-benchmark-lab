# retail_sql_001 — Find top repeat customers by category

**Category:** SQL analytics · **Difficulty:** medium · **Domain:** retail

## The problem

A retail business wants to know, per product category, which customers keep
coming back and how much they've spent. You're given three CSVs:

- `input/customers.csv` — id, name, email, `is_test_customer` flag, signup date
- `input/products.csv` — id, name, category
- `input/orders.csv` — id, customer, product, date, quantity, unit price, status

Write SQL that finds every "repeat" customer per category (more than one
valid order in that category) within the trailing 12 months as of
2024-06-01, ranked by total spend, highest first.

A valid order excludes:
- Cancelled orders (`status = 'cancelled'`)
- Orders from test customers (`is_test_customer = true`)
- Orders outside 2023-06-01–2024-05-31

## Expected output

See `expected/expected_output.csv`. Columns: `category, customer_id,
customer_name, order_count, total_spend`.

## Why this dataset is small

19 order rows is enough to exercise every rule (date filtering, cancelled
orders, test-customer exclusion, the ">1 order" repeat threshold, and
cross-category ranking) while staying hand-verifiable — you can check the
expected output by eye against `input/orders.csv`. Larger, messier retail
datasets will be added as separate harder tasks rather than making this one
bigger.

## Status

Live end to end. Try it: `arena run --task retail_sql_001 --agent baseline`
runs the checked-in baseline solution through the DuckDB connector and
diffs it against `expected/expected_output.csv` — see
[ROADMAP.md](../../../ROADMAP.md).
