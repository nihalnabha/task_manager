import sqlite3
from typing import List, Tuple
import hashlib


DB_NAME = "tasks.db"

def setup_db():
    """Create the tasks table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            description TEXT DEFAULT 'No description',
            completed INTEGER DEFAULT 0
        )
    """)
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Check if admin user exists, and add it if not
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        default_username = "admin"
        default_password = "admin123"
        hashed_password = hashlib.sha256(default_password.encode()).hexdigest()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (default_username, hashed_password))
        print(f"Default admin user created: Username: {default_username}, Password: {default_password}")

    conn.commit()
    conn.close()

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

def update_task(task_id: int, task: str, description: str, completed: int):
    """Update a task by its ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET task = ?, description = ?, completed = ? WHERE id = ?", 
                   (task, description, completed, task_id))
    conn.commit()
    conn.close()
