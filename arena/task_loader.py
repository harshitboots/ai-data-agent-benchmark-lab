from pathlib import Path

import yaml

from arena.config import TASK_FILE_GLOB, TASKS_DIR
from arena.schema import TaskSpec


class TaskNotFoundError(Exception):
    pass


def load_task(task_yaml_path: Path) -> TaskSpec:
    with open(task_yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return TaskSpec(**data)


def discover_tasks(root: Path = TASKS_DIR) -> list[tuple[Path, TaskSpec]]:
    """Find every task.yaml under root (category/task_id/task.yaml) and parse it."""
    return [
        (task_yaml.parent, load_task(task_yaml))
        for task_yaml in sorted(root.glob(TASK_FILE_GLOB))
    ]


def load_task_by_id(task_id: str, root: Path = TASKS_DIR) -> TaskSpec:
    for _, task in discover_tasks(root):
        if task.id == task_id:
            return task
    raise TaskNotFoundError(f"No task found with id '{task_id}'")
