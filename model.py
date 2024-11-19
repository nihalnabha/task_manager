from dataclasses import dataclass

@dataclass
class Task:
    id: int
    task: str
    description: str
    completed: bool

    def __str__(self):
        status = "Done" if self.completed else "Not Done"
        description_display = self.description if self.description != 'No description' else "No description provided"
        return f"ID: {self.id}, Task: {self.task}, Description: {description_display}, Status: {status}"
