from arena.task_loader import find_task
from connectors import duckdb as duckdb_connector


def test_run_sql_registers_input_files_as_tables():
    task_dir, task = find_task("retail_sql_001")
    result = duckdb_connector.run_sql(
        "SELECT COUNT(*) AS n FROM customers", task_dir / "input", task.input_files
    )
    assert result["n"].iloc[0] == 8


def test_run_sql_can_join_across_registered_tables():
    task_dir, task = find_task("retail_sql_001")
    result = duckdb_connector.run_sql(
        "SELECT COUNT(*) AS n FROM orders o JOIN products p ON p.product_id = o.product_id",
        task_dir / "input",
        task.input_files,
    )
    assert result["n"].iloc[0] == 19
