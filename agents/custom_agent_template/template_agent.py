from pathlib import Path

from arena.agent import AgentOutput, BaseAgent
from arena.schema import TaskSpec


class TemplateAgent(BaseAgent):
    """Copy this class into your own agents/<your_agent>/ folder and fill in run()."""

    def run(self, task: TaskSpec, input_dir: Path) -> AgentOutput:
        # task.description has the plain-language prompt; input_dir holds
        # every file listed in task.input_files. Return the SQL you produced
        # (for sql_analytics tasks) plus an explanation, or set `error` if
        # your agent couldn't produce an answer.
        raise NotImplementedError
