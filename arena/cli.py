import subprocess
from importlib.metadata import version as pkg_version

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from arena.config import TASK_FILE_GLOB, TASKS_DIR
from arena.leaderboard import build_leaderboard
from arena.runner import AgentNotFoundError, UnsupportedCategoryError, run_task, submit_run
from arena.scoring import RunResult, load_latest_run
from arena.task_loader import TaskNotFoundError, discover_tasks, load_task, load_task_by_id

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="AI Data Agent Benchmark Lab CLI",
)
console = Console()


@app.command("list-tasks")
def list_tasks() -> None:
    """List all benchmark tasks discovered under tasks/."""
    tasks = discover_tasks()
    if not tasks:
        console.print("[yellow]No tasks found under tasks/.[/yellow]")
        raise typer.Exit(code=0)

    table = Table(title="Available Tasks")
    table.add_column("ID")
    table.add_column("Category")
    table.add_column("Difficulty")
    table.add_column("Domain")
    for _, task in sorted(tasks, key=lambda pair: pair[1].id):
        table.add_row(task.id, task.category, task.difficulty, task.domain)
    console.print(table)


@app.command("show-task")
def show_task(task_id: str) -> None:
    """Show full details for a single task."""
    try:
        task = load_task_by_id(task_id)
    except TaskNotFoundError as exc:
        console.print(Panel(str(exc), title="Task not found", border_style="red"))
        raise typer.Exit(code=1)

    body = [
        f"Category:    {task.category}",
        f"Difficulty:  {task.difficulty}",
        f"Domain:      {task.domain}",
        f"Tools:       {', '.join(task.tools_allowed)}",
        f"Input files: {', '.join(task.input_files)}",
        f"Time limit:  {task.time_limit_seconds}s",
        f"Max cost:    ${task.max_cost_usd}",
        "",
        task.description.strip(),
        "",
        "[bold]Success criteria:[/bold]",
        *[f"  - {criterion}" for criterion in task.success_criteria],
    ]
    console.print(Panel("\n".join(body), title=f"{task.id} — {task.title}", border_style="cyan"))


@app.command("validate-tasks")
def validate_tasks() -> None:
    """Validate every task.yaml under tasks/ against the TaskSpec schema."""
    task_files = sorted(TASKS_DIR.glob(TASK_FILE_GLOB))
    if not task_files:
        console.print("[yellow]No task.yaml files found under tasks/.[/yellow]")
        raise typer.Exit(code=0)

    failures: list[tuple[str, str]] = []
    for task_yaml in task_files:
        rel_path = task_yaml.relative_to(TASKS_DIR)
        try:
            load_task(task_yaml)
        except Exception as exc:  # noqa: BLE001 - report any schema/parse error, then continue
            failures.append((str(rel_path), str(exc)))

    passed = len(task_files) - len(failures)
    console.print(f"Checked {len(task_files)} task file(s): {passed} passed, {len(failures)} failed.")
    for rel_path, error in failures:
        console.print(Panel(error, title=str(rel_path), border_style="red"))

    if failures:
        raise typer.Exit(code=1)


def _render_run_result(result: RunResult) -> None:
    header = (
        f"Task: {result.task_id}    Agent: {result.agent_name}    "
        f"Category: {result.category}    Elapsed: {result.elapsed_seconds:.2f}s"
    )
    console.print(header)
    if result.error:
        console.print(Panel(result.error, title="Agent error", border_style="red"))

    table = Table(title="Score breakdown")
    table.add_column("Dimension")
    table.add_column("Score", justify="right")
    table.add_column("Detail")
    for name, dimension in result.dimensions.items():
        table.add_row(name, str(dimension.score), dimension.detail)
    console.print(table)
    console.print(f"[bold]Final score: {result.final_score:.1f} / 100[/bold]")


def _default_submitted_by() -> str:
    try:
        name = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        return name or "anonymous"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "anonymous"


@app.command("run")
def run(
    task: str = typer.Option(..., "--task", help="Task ID, e.g. retail_sql_001"),
    agent: str = typer.Option("baseline", "--agent", help="Agent to run, e.g. baseline"),
    submit: bool = typer.Option(
        False, "--submit", help="Also write this run into leaderboard/submissions/"
    ),
    submitted_by: str | None = typer.Option(
        None, "--submitted-by", help="Name to submit under (defaults to `git config user.name`)"
    ),
) -> None:
    """Run an agent against a task and score the result."""
    try:
        result = run_task(task, agent)
    except (TaskNotFoundError, AgentNotFoundError, UnsupportedCategoryError) as exc:
        console.print(Panel(str(exc), title="Run failed", border_style="red"))
        raise typer.Exit(code=1)

    _render_run_result(result)

    if submit:
        who = submitted_by or _default_submitted_by()
        path = submit_run(result, who)
        console.print(f"Submitted as [bold]{who}[/bold] -> {path}")


@app.command("score")
def score(
    run_id: str = typer.Option("latest", "--run", help="Which run to score (only 'latest' is supported today)"),
) -> None:
    """Show the score breakdown for a previous run."""
    if run_id != "latest":
        console.print(
            Panel(
                f"'{run_id}' is not supported — only 'latest' is supported today.",
                title="Unsupported --run value",
                border_style="red",
            )
        )
        raise typer.Exit(code=1)

    try:
        result = load_latest_run()
    except FileNotFoundError as exc:
        console.print(Panel(str(exc), title="No runs found", border_style="red"))
        raise typer.Exit(code=1)

    _render_run_result(result)


@app.command("leaderboard")
def leaderboard(
    task: str | None = typer.Option(None, "--task", help="Only show this task's rankings"),
) -> None:
    """Regenerate leaderboard/results.json + leaderboard.md from submissions and display it."""
    data = build_leaderboard()

    if not data:
        console.print(
            "[yellow]No submissions yet — run `arena run --task ... --agent ... --submit` "
            "or see leaderboard/submissions/README.md.[/yellow]"
        )
        raise typer.Exit(code=0)

    task_ids = [task] if task else sorted(data)
    for task_id in task_ids:
        entries = data.get(task_id)
        if not entries:
            console.print(f"[yellow]No submissions for '{task_id}'.[/yellow]")
            continue

        table = Table(title=task_id)
        table.add_column("Rank", justify="right")
        table.add_column("Agent")
        table.add_column("Score", justify="right")
        table.add_column("Submitted by")
        table.add_column("Timestamp")
        for entry in entries:
            table.add_row(
                str(entry.rank),
                entry.agent_name,
                f"{entry.final_score:.1f}",
                entry.submitted_by,
                entry.timestamp,
            )
        console.print(table)


@app.command("version")
def show_version() -> None:
    """Show the installed CLI version."""
    console.print(f"arena {pkg_version('ai-data-agent-benchmark-lab')}")


if __name__ == "__main__":
    app()
