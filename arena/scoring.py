import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from arena.config import RUNS_DIR


@dataclass
class DimensionResult:
    """A single scored dimension (execution, correctness, ...)."""

    score: int
    detail: str


@dataclass
class RunResult:
    task_id: str
    agent_name: str
    category: str
    dimensions: dict[str, DimensionResult]
    final_score: float
    elapsed_seconds: float
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )
    error: str | None = None


def save_run(result: RunResult) -> Path:
    """Write a run result to runs/ and return the file path."""
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    safe_timestamp = result.timestamp.replace(":", "-")
    path = RUNS_DIR / f"{safe_timestamp}__{result.task_id}__{result.agent_name}.json"

    payload = asdict(result)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def load_latest_run() -> RunResult:
    """Load the most recently written run result from runs/."""
    if not RUNS_DIR.exists():
        raise FileNotFoundError("No runs found — run `arena run` first.")

    run_files = sorted(RUNS_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime)
    if not run_files:
        raise FileNotFoundError("No runs found — run `arena run` first.")

    data = json.loads(run_files[-1].read_text(encoding="utf-8"))
    data["dimensions"] = {
        name: DimensionResult(**dim) for name, dim in data["dimensions"].items()
    }
    return RunResult(**data)
