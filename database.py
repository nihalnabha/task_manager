import sqlite3
import hashlib
from typing import List, Tuple

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
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Hash the provided password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Query to check if the user exists with the given username and password
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()

    conn.close()
    return user is not None

def add_user(username: str, password: str):
    """Add a new user to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Hash the password before storing
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print(f"User '{username}' added successfully!")
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' already exists.")
    
    conn.close()

# Other task-related functions
def add_task(task: str, description: str = None):
    """Add a task to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    description = description or 'No description'  # Use default if description is None
    cursor.execute("INSERT INTO tasks (task, description, completed) VALUES (?, ?, ?)", (task, description, 0))
    conn.commit()
    conn.close()

def get_tasks() -> List[Tuple[int, str, str, int]]:
    """Retrieve all tasks from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, description, completed FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(task_id: int):
    """Delete a task by its ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def update_task(task_id: int, description: str, completed: int):
    """Update a task's description and completion status by its ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Update only the description and completed fields, leaving 'task' unchanged
    cursor.execute("UPDATE tasks SET description = ?, completed = ? WHERE id = ?",
                   (description, completed, task_id))  # Corrected parameter order and removed 'task'
    
    conn.commit()
    conn.close()


