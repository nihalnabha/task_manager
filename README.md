Task Manager CLI Application
A simple and interactive command-line application to manage tasks with user authentication, built using Python and SQLite. The app supports adding, updating, deleting, and displaying tasks, with features like authentication and session management for multiple users.

Features
User Authentication:

Secure login system using hashed passwords.
Session management for logged-in users.
Task Management:

Add tasks with optional descriptions.
Update task details and completion status.
Delete tasks by their unique IDs.
View all tasks in a tabular format using the rich library.
Database Integration:

Persistent task storage with SQLite.
Automatic database setup for first-time use.
Requirements
Make sure you have the following installed:

Python 3.7 or later
Required Python libraries:
typer
rich
Install dependencies using pip:

bash
Copy code
pip install typer rich
How to Run
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/task-manager-cli.git
cd task-manager-cli
Initialize the Database: Run the following command to set up the database:

bash
Copy code
python task.py init
Start Using the CLI:

Add a new task:
bash
Copy code
python task.py add
Show all tasks:
bash
Copy code
python task.py show
Update a task:
bash
Copy code
python task.py update
Delete a task:
bash
Copy code
python task.py delete
Logout: To log out of the application, run:

bash
Copy code
python task.py logout
Application Commands
Command	Description
init	Initialize the database
add	Add a new task
show	Show all tasks
update	Update an existing task
delete	Delete a task by ID
logout	Logout from the current session
Project Structure
bash
Copy code
task-manager-cli/
│
├── task.py       # Main CLI application
├── database.py   # Database setup and helper functions
├── model.py      # Task model definition
└── README.md     # Project documentation
Future Enhancements
Add due dates and priorities for tasks.
Enable exporting tasks to a CSV file.
Add email notifications for reminders.
