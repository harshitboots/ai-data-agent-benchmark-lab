from pathlib import Path

import pandas as pd

from arena.agent import AgentOutput
from arena.schema import TaskSpec
from arena.scoring import DimensionResult
from connectors import duckdb as duckdb_connector


def _results_match(actual: pd.DataFrame, expected: pd.DataFrame) -> tuple[bool, str]:
    if list(actual.columns) != list(expected.columns):
        return False, f"column mismatch: got {list(actual.columns)}, expected {list(expected.columns)}"
    if len(actual) != len(expected):
        return False, f"row count mismatch: got {len(actual)}, expected {len(expected)}"

    actual = actual.reset_index(drop=True)
    expected = expected.reset_index(drop=True)
    for col in expected.columns:
        if pd.api.types.is_numeric_dtype(expected[col]):
            if not actual[col].astype(float).round(6).equals(expected[col].astype(float).round(6)):
                return False, f"value mismatch in column '{col}'"
        elif not actual[col].astype(str).equals(expected[col].astype(str)):
            return False, f"value mismatch in column '{col}'"

    return True, "output matches expected_output exactly"


def evaluate(
    task: TaskSpec,
    task_dir: Path,
    agent_output: AgentOutput,
    elapsed_seconds: float,
) -> dict[str, DimensionResult]:
    """Score an agent's SQL output for a sql_analytics task against expected_output."""
    if agent_output.error or not agent_output.sql:
        detail = agent_output.error or "agent produced no SQL"
        zero = DimensionResult(score=0, detail=detail)
        return {
            "execution": zero,
            "correctness": zero,
            "efficiency": zero,
            "explanation": DimensionResult(score=0, detail="no explanation provided"),
            "cost_latency": zero,
        }

    input_dir = task_dir / "input"
    try:
        actual = duckdb_connector.run_sql(agent_output.sql, input_dir, task.input_files)
    except Exception as exc:  # noqa: BLE001 - any SQL/runtime error means execution failed
        error_detail = f"SQL failed to execute: {exc}"
        zero = DimensionResult(score=0, detail=error_detail)
        return {
            "execution": zero,
            "correctness": zero,
            "efficiency": zero,
            "explanation": DimensionResult(score=0, detail="no explanation provided"),
            "cost_latency": zero,
        }

    execution = DimensionResult(score=100, detail="SQL executed successfully")
    efficiency = DimensionResult(
        score=100,
        detail="efficiency scoring is currently tied to execution success (v1 placeholder)",
    )

    expected_path = task_dir / "expected" / task.expected_output
    expected = pd.read_csv(expected_path)
    matched, detail = _results_match(actual, expected)
    correctness = DimensionResult(score=100 if matched else 0, detail=detail)

    explanation = DimensionResult(
        score=100 if agent_output.explanation.strip() else 0,
        detail=agent_output.explanation or "no explanation provided",
    )

    within_budget = (
        agent_output.cost_usd <= task.max_cost_usd and elapsed_seconds <= task.time_limit_seconds
    )
    cost_latency = DimensionResult(
        score=100 if within_budget else 0,
        detail=f"cost=${agent_output.cost_usd:.4f}, elapsed={elapsed_seconds:.2f}s "
        f"(budget: ${task.max_cost_usd}, {task.time_limit_seconds}s)",
    )

    return {
        "execution": execution,
        "correctness": correctness,
        "efficiency": efficiency,
        "explanation": explanation,
        "cost_latency": cost_latency,
    }
