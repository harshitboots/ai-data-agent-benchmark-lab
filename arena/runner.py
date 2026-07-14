import time

from agents.baseline_agent import BaselineAgent
from arena.agent import BaseAgent
from arena.scoring import RunResult, save_run
from arena.task_loader import TaskNotFoundError, find_task
from evaluators import sql_evaluator
from evaluators.final_score import compute_final_score

AGENT_REGISTRY: dict[str, type[BaseAgent]] = {
    "baseline": BaselineAgent,
}

EVALUATOR_REGISTRY = {
    "sql_analytics": sql_evaluator.evaluate,
}


class AgentNotFoundError(Exception):
    pass


class UnsupportedCategoryError(Exception):
    pass


def run_task(task_id: str, agent_name: str) -> RunResult:
    """Run agent_name against task_id, score it, save the run, and return the result."""
    task_dir, task = find_task(task_id)

    if agent_name not in AGENT_REGISTRY:
        raise AgentNotFoundError(
            f"No agent registered as '{agent_name}'. Available: {', '.join(AGENT_REGISTRY)}"
        )
    if task.category not in EVALUATOR_REGISTRY:
        raise UnsupportedCategoryError(
            f"No evaluator implemented yet for category '{task.category}'"
        )

    agent = AGENT_REGISTRY[agent_name]()
    evaluate = EVALUATOR_REGISTRY[task.category]

    start = time.monotonic()
    agent_output = agent.run(task, task_dir / "input")
    elapsed_seconds = time.monotonic() - start

    dimensions = evaluate(task, task_dir, agent_output, elapsed_seconds)
    final_score = compute_final_score(task.scoring, dimensions)

    result = RunResult(
        task_id=task.id,
        agent_name=agent_name,
        category=task.category,
        dimensions=dimensions,
        final_score=final_score,
        elapsed_seconds=elapsed_seconds,
        error=agent_output.error,
    )
    save_run(result)
    return result


__all__ = [
    "AgentNotFoundError",
    "UnsupportedCategoryError",
    "TaskNotFoundError",
    "run_task",
]
