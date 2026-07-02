import pytest

from arena.task_loader import TaskNotFoundError, discover_tasks, load_task_by_id


def test_discover_tasks_finds_retail_sql_001():
    tasks = discover_tasks()
    ids = [task.id for _, task in tasks]
    assert "retail_sql_001" in ids


def test_discover_tasks_skips_template():
    tasks = discover_tasks()
    ids = [task.id for _, task in tasks]
    assert "category_shortname_001" not in ids


def test_load_task_by_id_returns_matching_task():
    task = load_task_by_id("retail_sql_001")
    assert task.category == "sql_analytics"
    assert task.domain == "retail"
    assert task.scoring.execution + task.scoring.correctness + task.scoring.efficiency \
        + task.scoring.explanation + task.scoring.cost_latency == 100


def test_load_task_by_id_raises_for_unknown_id():
    with pytest.raises(TaskNotFoundError):
        load_task_by_id("does_not_exist_001")
