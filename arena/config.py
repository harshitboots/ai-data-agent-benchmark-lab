from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = PROJECT_ROOT / "tasks"
DATASETS_DIR = PROJECT_ROOT / "datasets"
RUNS_DIR = PROJECT_ROOT / "runs"
LEADERBOARD_DIR = PROJECT_ROOT / "leaderboard"
SUBMISSIONS_DIR = LEADERBOARD_DIR / "submissions"

TASK_FILE_GLOB = "*/*/task.yaml"
