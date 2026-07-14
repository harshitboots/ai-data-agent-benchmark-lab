from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from arena.schema import TaskSpec


@dataclass
class AgentOutput:
    """What an agent hands back for a single task attempt."""

    sql: str | None = None
    explanation: str = ""
    cost_usd: float = 0.0
    error: str | None = None


class BaseAgent(ABC):
    """Interface every agent (baseline, OpenAI, Anthropic, custom, ...) implements."""

    @abstractmethod
    def run(self, task: TaskSpec, input_dir: Path) -> AgentOutput:
        """Attempt the task using the files in input_dir and return an AgentOutput."""
        raise NotImplementedError
