import os
import typer
from rich.console import Console
from rich.table import Table
from database import setup_db, add_task, get_tasks, delete_task, update_task, authenticate_user
from model import Task  # Import Task class from model.py

# Session management functions
SESSION_FILE = "session.txt"

def is_logged_in():
    """Check if the user is logged in by checking the existence of the session file."""
    return os.path.exists(SESSION_FILE)

def login_user(username):
    """Store the logged-in user's session."""
    with open(SESSION_FILE, "w") as f:
        f.write(username)

def logout_user():
    """Remove the logged-in user's session (log out)."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        typer.echo("You have been logged out.")

def get_logged_in_user():
    """Retrieve the currently logged-in user from the session file."""
    if is_logged_in():
        with open(SESSION_FILE, "r") as f:
            return f.read().strip()
    return None

def authenticate():
    """Authenticate user. If already logged in, skip prompt."""
    if is_logged_in():
        username = get_logged_in_user()
        typer.echo(f"Welcome back, {username}!")
        return True  # User is logged in
    else:
        username = input("Enter username: ")
        password = input("Enter password: ")
        if authenticate_user(username, password):  # Check credentials against the database
            typer.echo(f"Welcome, {username}!")
            login_user(username)  # Save the session
            return True
        else:
            typer.echo("Authentication failed. Exiting.")
            return False

# CLI app setup
console = Console()
app = typer.Typer()

# Command to log out
@app.command(short_help="Logs out the current user")
def logout():
    """Logs the user out by removing the session file."""
    if not is_logged_in():
        typer.echo("No user is currently logged in.")
        raise typer.Exit()
    logout_user()  # Log out by removing the session file
    typer.echo("You have been logged out.")

# Command to add a task
@app.command(short_help="Adds an item")
def add():
    if not authenticate():  # Check if user is authenticated before performing any action
        raise typer.Exit()  # Exit if authentication fails
    task = input("Enter the task: ")
    description = input("Enter the description (leave empty for default): ")
    add_task(task, description)
    typer.echo(f"Task '{task}' with description '{description}' added successfully!")
    show()

# Command to delete a task
@app.command(short_help="Deletes an item")
def delete():
    if not authenticate():  # Check if user is authenticated before performing any action
        raise typer.Exit()  # Exit if authentication fails
    task_id = int(input("Enter the ID of the task to delete: "))
    delete_task(task_id)
    typer.echo(f"Task with ID {task_id} deleted successfully!")
    show()

# Command to update a task
@app.command(short_help="Updates an item")
def update():
    """Update the task description and completion status."""
    if not is_logged_in():  # Check if user is authenticated
        typer.echo("You need to log in first.")
        raise typer.Exit()

    # Prompt for task ID to update
    task_id = int(input("Enter the ID of the task to update: "))

    # Prompt for new description (if left blank, use the default value)
    new_description = input("Enter the new description (leave empty for default): ")

    # Prompt for task completion status (1 for completed, 0 for not completed)
    completed = int(input("Is the task completed? (1 for Yes, 0 for No): "))

    # Update only the description and completed status of the task
    update_task(task_id, new_description or 'No description', completed)

    # Notify the user of the successful update
    typer.echo(f"Task with ID {task_id} updated successfully!")

    # Show the updated list of tasks
    show()

# Command to show all tasks
@app.command(short_help="Shows all tasks")
def show():
    if not authenticate():  # Check if user is authenticated before performing any action
        raise typer.Exit()  # Exit if authentication fails
    tasks = get_tasks()

    console.print("[bold magenta]Arise, awake, and stop not till the goal is reached![/bold magenta]")

    # Create a table to display the tasks
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Id", style="dim", width=6)
    table.add_column("Task", min_width=20)
    table.add_column("Description", min_width=12, justify="right")
    table.add_column("Status", min_width=12, justify="right")

    for task in tasks:
        # Convert each task into a Task object
        task_obj = Task(id=task[0], task=task[1], description=task[2], completed=task[3])
        table.add_row(str(task_obj.id), task_obj.task, task_obj.description, "Done" if task_obj.completed else "Not Done")

    console.print(table)

# Command to initialize the database
@app.command(short_help="Initialize the database")
def init():
    setup_db()
    typer.echo("Database initialized successfully!")

# Main entry point for the CLI
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Main entry point for the CLI."""
    if ctx.invoked_subcommand is None:  # Check if no subcommand is invoked
        if not authenticate():  # Authenticate user before proceeding
            raise typer.Exit()  # Exit if authentication fails
        console.print("\n[bold magenta]Available Commands:[/bold magenta]")
        console.print("- [bold green]add[/bold green]: Adds a new task.")
        console.print("- [bold green]delete[/bold green]: Deletes an existing task.")
        console.print("- [bold green]update[/bold green]: Updates a task.")
        console.print("- [bold green]show[/bold green]: Displays all tasks.")
        console.print("- [bold green]init[/bold green]: Initialize the database.")
        console.print("- [bold red]logout[/bold red]: Logs out the current user.")  # Show logout option
        console.print("\nUse 'python task.py **command**' to execute a command.")

# Run the CLI app
if __name__ == "__main__":
    app()
