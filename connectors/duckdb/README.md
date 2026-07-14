# duckdb

DuckDB connector used by SQL tasks. `run_sql(sql, input_dir, input_files)`
(see [`__init__.py`](__init__.py)) loads each input CSV with pandas,
registers it into an in-memory DuckDB connection as a table named by the
file's stem (`customers.csv` → `customers`), runs the query, and returns a
DataFrame. Used by [`evaluators/sql_evaluator.py`](../../evaluators/sql_evaluator.py).

See [ROADMAP.md](../../ROADMAP.md) for the phase plan.

