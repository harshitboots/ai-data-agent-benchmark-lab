from pathlib import Path

import duckdb
import pandas as pd


def run_sql(sql: str, input_dir: Path, input_files: list[str]) -> pd.DataFrame:
    """Run sql against the given input CSVs, each registered as a view named by its stem."""
    conn = duckdb.connect(":memory:")
    try:
        for filename in input_files:
            table_name = Path(filename).stem
            # duckdb's own CSV reader (rather than pandas.read_csv) so date-like
            # columns are inferred as DATE, not VARCHAR.
            conn.read_csv(str(input_dir / filename)).create_view(table_name)
        return conn.execute(sql).fetchdf()
    finally:
        conn.close()
