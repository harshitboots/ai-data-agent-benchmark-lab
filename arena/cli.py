from importlib.metadata import version as pkg_version

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from arena.config import TASK_FILE_GLOB, TASKS_DIR
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


@app.command("version")
def show_version() -> None:
    """Show the installed CLI version."""
    console.print(f"arena {pkg_version('ai-data-agent-benchmark-lab')}")


if __name__ == "__main__":
    app()
