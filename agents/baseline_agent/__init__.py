from pathlib import Path

from arena.agent import AgentOutput, BaseAgent
from arena.schema import TaskSpec

SOLUTIONS_DIR = Path(__file__).parent / "solutions"


class BaselineAgent(BaseAgent):
    """Deterministic, no-LLM agent: looks up a known-correct SQL solution per task.

    Used as the scoring floor — it has no reasoning, so it always scores 0 on
    the explanation dimension. If a task has no known solution yet, it fails
    cleanly rather than crashing.
    """

    def run(self, task: TaskSpec, input_dir: Path) -> AgentOutput:
        solution_path = SOLUTIONS_DIR / f"{task.id}.sql"
        if not solution_path.exists():
            return AgentOutput(error=f"no baseline solution available for task '{task.id}'")
        return AgentOutput(sql=solution_path.read_text(encoding="utf-8"))
