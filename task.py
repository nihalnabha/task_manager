import typer
from rich.console import Console
from rich.table import Table
from database import setup_db, add_task, get_tasks, delete_task, update_task, authenticate_user
from model import Task

console = Console()
app = typer.Typer()
is_authenticated = False  # Track session authentication status

def login():
    """Authenticate the user."""
    global is_authenticated
    username = input("Enter username: ")
    password = input("Enter password: ")
    if authenticate_user(username, password):
        typer.echo(f"Welcome, {username}!")
        is_authenticated = True
    else:
        typer.echo("Invalid username or password. Please try again.")
        raise typer.Exit()

@app.command(short_help="Adds an item")
def add():
    if not is_authenticated:
        typer.echo("You need to log in first.")
        raise typer.Exit()
    task = input("Enter the task: ")
    description = input("Enter the description (leave empty for default): ")
    add_task(task, description)
    typer.echo(f"Task '{task}' with description '{description}' added successfully!")
    show()

@app.command(short_help="Deletes an item")
def delete():
    if not is_authenticated:
        typer.echo("You need to log in first.")
        raise typer.Exit()
    task_id = int(input("Enter the ID of the task to delete: "))
    delete_task(task_id)
    typer.echo(f"Task with ID {task_id} deleted successfully!")
    show()

@app.command(short_help="Updates an item")
def update():
    if not is_authenticated:
        typer.echo("You need to log in first.")
        raise typer.Exit()
    task_id = int(input("Enter the ID of the task to update: "))
    new_task = input("Enter the new task: ")
    new_description = input("Enter the new description (leave empty for default): ")
    completed = int(input("Is the task completed? (1 for Yes, 0 for No): "))
    update_task(task_id, new_task, new_description or 'No description', completed)
    typer.echo(f"Task with ID {task_id} updated successfully!")
    show()

@app.command(short_help="Shows all tasks")
def show():
    if not is_authenticated:
        typer.echo("You need to log in first.")
        raise typer.Exit()
    tasks = get_tasks()
    console.print("[bold magenta]Arise, awake, and stop not till the goal is reached![/bold magenta]")



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

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Main entry point for the CLI."""
    if ctx.invoked_subcommand is None:
        login()
        console.print("\n[bold magenta]Available Commands:[/bold magenta]")
        console.print("- [bold green]add[/bold green]: Add a new task.")
        console.print("- [bold green]delete[/bold green]: Delete an existing task.")
        console.print("- [bold green]update[/bold green]: Update a task.")
        console.print("- [bold green]show[/bold green]: Display all tasks.")
        console.print("- [bold green]init[/bold green]: Initialize the database.")
        console.print("\nUse 'python task.py [command]' to execute a command.")

if __name__ == "__main__":
    app()
