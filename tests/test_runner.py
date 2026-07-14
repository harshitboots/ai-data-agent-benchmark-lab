import pytest

from arena.runner import AgentNotFoundError, run_task
from arena.task_loader import TaskNotFoundError


def test_run_task_baseline_scores_ninety_on_retail_sql_001():
    result = run_task("retail_sql_001", "baseline")

    assert result.error is None
    assert result.dimensions["correctness"].score == 100
    assert result.dimensions["explanation"].score == 0  # baseline never explains itself
    # weights: execution 30, correctness 40, efficiency 10, explanation 10, cost_latency 10
    assert result.final_score == pytest.approx(90.0)


def test_run_task_raises_for_unknown_task():
    with pytest.raises(TaskNotFoundError):
        run_task("does_not_exist_001", "baseline")


def test_run_task_raises_for_unknown_agent():
    with pytest.raises(AgentNotFoundError):
        run_task("retail_sql_001", "not_a_real_agent")
