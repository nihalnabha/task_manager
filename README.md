
## Steps to Use the Application


1. Clone the Repository
```bash
git clone https://github.com/yourusername/task_manager.git
cd task_manager
```
2. Install Dependencies
    Make sure you have Python installed. Install the required libraries using pip:

```bash
pip install typer rich
```
3. Initialize the Database
    Before using the application, initialize the database:

```bash
python task.py init
```
4. Log In to the Application
    When you run any command, you’ll be prompted to log in. Use the default admin credentials for the first time
```bash
Username: admin
Password: admin123
```
5. Available Commands
    Use the following commands to interact with the application:
```bash
Command	Description
python task.py  add	       Add a new task.
python task.py show	       Display all tasks in a table format.
python task.py update	   Update a task's description or status.
python task.py delete	   Delete a task by its ID.
python task.py logout	   Log out from the application.
```
6. Example Usage
    
    Add a Task:
 ```bash
python task.py add
```
Enter the task name and description when prompted.
 

Show All Tasks:
 ```bash
python task.py show
```
Enter the task ID, new description, and completion status.

Update a Task:
 ```bash
python task.py update
```
Enter the task ID, new description, and completion status.

Delete a Task:

 ```bash
python task.py delete
```
Enter the task ID to remove it from the database.


Log Out:
 ```bash
python task.py logout
```




