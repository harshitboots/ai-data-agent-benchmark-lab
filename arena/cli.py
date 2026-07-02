import typer
from rich.console import Console
from rich.table import Table

from arena.task_loader import TaskNotFoundError, discover_tasks, load_task_by_id

app = typer.Typer(add_completion=False, help="AI Data Agent Benchmark Lab CLI")
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
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1)

    console.print(f"[bold]{task.id}[/bold] — {task.title}")
    console.print(f"Category:    {task.category}")
    console.print(f"Difficulty:  {task.difficulty}")
    console.print(f"Domain:      {task.domain}")
    console.print(f"Tools:       {', '.join(task.tools_allowed)}")
    console.print(f"Input files: {', '.join(task.input_files)}")
    console.print(f"Time limit:  {task.time_limit_seconds}s")
    console.print(f"Max cost:    ${task.max_cost_usd}")
    console.print()
    console.print(task.description.strip())
    console.print()
    console.print("[bold]Success criteria:[/bold]")
    for criterion in task.success_criteria:
        console.print(f"  - {criterion}")


if __name__ == "__main__":
    app()
