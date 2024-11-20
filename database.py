import sqlite3
import hashlib
from typing import List, Tuple

# Name of the SQLite database file
DB_NAME = "tasks.db"

def setup_db():
    """Create the tasks and users tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create the tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            description TEXT DEFAULT 'No description',
            completed INTEGER DEFAULT 0
        )
    """)

    # Create the users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Add a default admin user if no users exist
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        default_username = "admin"
        default_password = "admin123"
        hashed_password = hashlib.sha256(default_password.encode()).hexdigest()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (default_username, hashed_password))
        print(f"Default admin user created: Username: {default_username}, Password: {default_password}")

    conn.commit()
    conn.close()


def authenticate_user(username: str, password: str) -> bool:
    """Authenticate a user by their username and password."""
    conn = sqlite3.connect(DB_NAME)  # Connect to the SQLite database
    cursor = conn.cursor()

    # Hash the provided password for comparison
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Query to check if the user exists with the given username and password
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", 
                   (username, hashed_password))
    user = cursor.fetchone()  # Fetch the result

    conn.close()  # Close the database connection
    return user is not None  # Return True if a matching user is found, else False

def add_user(username: str, password: str):
    """Add a new user to the database."""
    conn = sqlite3.connect(DB_NAME)  # Connect to the SQLite database
    cursor = conn.cursor()

    # Hash the password before storing it in the database
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        # Insert the new user into the 'users' table
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       (username, hashed_password))
        conn.commit()  # Save the changes
        print(f"User '{username}' added successfully!")
    except sqlite3.IntegrityError:
        # Handle the case where the username already exists
        print(f"Error: Username '{username}' already exists.")
    
    conn.close()  # Close the database connection

# Task-related functions
def add_task(task: str, description: str = None):
    """Add a task to the database."""
    conn = sqlite3.connect(DB_NAME)  # Connect to the SQLite database
    cursor = conn.cursor()

    # Use default description if none is provided
    description = description or 'No description'

    # Insert the new task into the 'tasks' table
    cursor.execute("INSERT INTO tasks (task, description, completed) VALUES (?, ?, ?)", 
                   (task, description, 0))  # Default completion status is 0 (not done)
    conn.commit()  # Save the changes
    conn.close()  # Close the database connection

def get_tasks() -> List[Tuple[int, str, str, int]]:
    """Retrieve all tasks from the database."""
    conn = sqlite3.connect(DB_NAME)  # Connect to the SQLite database
    cursor = conn.cursor()

    # Query to fetch all tasks
    cursor.execute("SELECT id, task, description, completed FROM tasks")
    tasks = cursor.fetchall()  # Fetch all results

    conn.close()  # Close the database connection
    return tasks  # Return the list of tasks

def delete_task(task_id: int):
    """Delete a task by its ID, and notify if the ID does not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if the task exists
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if not task:
        print(f"No task found with ID {task_id}.")  # Notify the user
    else:
        # If task exists, delete it
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        print(f"Task with ID {task_id} deleted successfully.")

    conn.close()

def update_task(task_id: int, description: str, completed: int):
    """Update a task's description and completion status by its ID."""
    conn = sqlite3.connect(DB_NAME)  # Connect to the SQLite database
    cursor = conn.cursor()

    # Update only the description and completed fields for the given task ID
    cursor.execute("UPDATE tasks SET description = ?, completed = ? WHERE id = ?", 
                   (description, completed, task_id))
    conn.commit()  # Save the changes
    conn.close()  # Close the database connection
