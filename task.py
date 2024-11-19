import typer
from rich.console import Console
from rich.table import Table
from database import setup_db, add_task, get_tasks, delete_task, update_task
from model import Task

console = Console()
app = typer.Typer()

@app.command(short_help="Adds an item")
def add():
    task = input("Enter the task: ")
    description = input("Enter the description (leave empty for default): ")
    add_task(task, description)
    typer.echo(f"Task '{task}' with description '{description}' added successfully!")
    show()

@app.command(short_help="Deletes an item")
def delete():
    task_id = int(input("Enter the ID of the task to delete: "))
    delete_task(task_id)
    typer.echo(f"Task with ID {task_id} deleted successfully!")
    show()

@app.command(short_help="Updates an item")
def update():
    task_id = int(input("Enter the ID of the task to update: "))
    new_task = input("Enter the new task: ")
    new_description = input("Enter the new description (leave empty for default): ")
    completed = int(input("Is the task completed? (1 for Yes, 0 for No): "))
    update_task(task_id, new_task, new_description or 'No description', completed)
    typer.echo(f"Task with ID {task_id} updated successfully!")
    show()

@app.command(short_help="Shows all tasks")
def show():
    tasks = get_tasks()
    console.print("[bold magenta]Todos[/bold magenta]!")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Id", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Description", min_width=12, justify="right")
    table.add_column("Status", min_width=12, justify="right")

    for task in tasks:
        description_display = task[2] if task[2] != 'No description' else "No description provided"
        done = "[green]1[/green]" if task[3] else "[red]0[/red]"
        table.add_row(str(task[0]), task[1], description_display, done)

    console.print(table)

@app.command(short_help="Initialize the database")
def init():
    setup_db()
    typer.echo("Database initialized successfully!")

if __name__ == "__main__":
    app()