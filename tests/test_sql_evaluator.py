from arena.agent import AgentOutput
from arena.config import PROJECT_ROOT
from arena.task_loader import find_task
from evaluators.sql_evaluator import evaluate

SOLUTION_SQL = (
    PROJECT_ROOT / "agents" / "baseline_agent" / "solutions" / "retail_sql_001.sql"
).read_text(encoding="utf-8")


def test_evaluate_scores_correct_solution_as_a_full_match():
    task_dir, task = find_task("retail_sql_001")
    agent_output = AgentOutput(sql=SOLUTION_SQL)

    dimensions = evaluate(task, task_dir, agent_output, elapsed_seconds=0.1)

    assert dimensions["execution"].score == 100
    assert dimensions["correctness"].score == 100
    assert dimensions["cost_latency"].score == 100


def test_evaluate_scores_wrong_output_as_zero_correctness():
    task_dir, task = find_task("retail_sql_001")
    agent_output = AgentOutput(sql="SELECT * FROM customers")

    dimensions = evaluate(task, task_dir, agent_output, elapsed_seconds=0.1)

    assert dimensions["execution"].score == 100
    assert dimensions["correctness"].score == 0


def test_evaluate_scores_broken_sql_as_zero_execution():
    task_dir, task = find_task("retail_sql_001")
    agent_output = AgentOutput(sql="SELECT * FROM not_a_real_table")

    dimensions = evaluate(task, task_dir, agent_output, elapsed_seconds=0.1)

    assert dimensions["execution"].score == 0
    assert dimensions["correctness"].score == 0


def test_evaluate_scores_agent_error_as_zero_everything():
    task_dir, task = find_task("retail_sql_001")
    agent_output = AgentOutput(error="agent gave up")

    dimensions = evaluate(task, task_dir, agent_output, elapsed_seconds=0.1)

    assert all(dim.score == 0 for dim in dimensions.values())
