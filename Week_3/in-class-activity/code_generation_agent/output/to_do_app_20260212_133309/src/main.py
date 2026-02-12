import json
import os
from typing import List, Dict, Optional

class TodoApp:
    def __init__(self, storage_file: str = "tasks.json"):
        self.storage_file = storage_file
        self.tasks: List[Dict] = []
        self.load_tasks()

    def load_tasks(self) -> None:
        """Load tasks from JSON file."""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    self.tasks = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []

    def save_tasks(self) -> None:
        """Save tasks to JSON file."""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except IOError as e:
            print(f"Error saving tasks: {e}")

    def add_task(self, description: str) -> Optional[int]:
        """Add a new task and return its ID."""
        if not description.strip():
            print("Error: Task description cannot be empty.")
            return None

        task_id = len(self.tasks) + 1
        task = {
            "id": task_id,
            "description": description.strip(),
            "completed": False
        }
        self.tasks.append(task)
        self.save_tasks()
        return task_id

    def list_tasks(self) -> None:
        """Display all tasks."""
        if not self.tasks:
            print("No tasks found.")
            return

        for task in self.tasks:
            status = "✓" if task["completed"] else "✗"
            print(f"{task['id']}. [{status}] {task['description']}")

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed."""
        task = self._find_task(task_id)
        if task:
            task["completed"] = True
            self.save_tasks()
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        task = self._find_task(task_id)
        if task:
            self.tasks.remove(task)
            # Reassign IDs to maintain continuity
            for i, task in enumerate(self.tasks):
                task["id"] = i + 1
            self.save_tasks()
            return True
        return False

    def _find_task(self, task_id: int) -> Optional[Dict]:
        """Find task by ID."""
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        print(f"Error: Task with ID {task_id} not found.")
        return None

def main():
    app = TodoApp()

    print("To-Do App")
    print("Commands: add <task>, list, complete <id>, delete <id>, exit")

    while True:
        command = input("\n> ").strip().split(maxsplit=1)

        if not command:
            continue

        cmd = command[0].lower()

        if cmd == "exit":
            print("Goodbye!")
            break

        elif cmd == "add":
            if len(command) < 2:
                print("Error: Task description required.")
                continue
            task_id = app.add_task(command[1])
            if task_id:
                print(f"Task added with ID: {task_id}")

        elif cmd == "list":
            app.list_tasks()

        elif cmd == "complete":
            if len(command) < 2:
                print("Error: Task ID required.")
                continue
            try:
                task_id = int(command[1])
                if app.complete_task(task_id):
                    print(f"Task {task_id} marked as completed.")
            except ValueError:
                print("Error: Invalid task ID.")

        elif cmd == "delete":
            if len(command) < 2:
                print("Error: Task ID required.")
                continue
            try:
                task_id = int(command[1])
                if app.delete_task(task_id):
                    print(f"Task {task_id} deleted.")
            except ValueError:
                print("Error: Invalid task ID.")

        else:
            print("Error: Unknown command. Available commands: add, list, complete, delete, exit")

if __name__ == "__main__":
    main()
