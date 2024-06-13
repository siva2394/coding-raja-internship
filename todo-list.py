import json
import os
from datetime import datetime

class Task:
    def __init__(self, description, priority='low', due_date=None, completed=False):
        self.description = description
        self.priority = priority
        self.due_date = due_date if isinstance(due_date, datetime) else self.parse_due_date(due_date)
        self.completed = completed

    def to_dict(self):
        return {
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed
        }

    @staticmethod
    def parse_due_date(due_date_str):
        if due_date_str:
            try:
                return datetime.fromisoformat(due_date_str)
            except ValueError:
                print(f"Invalid date format: {due_date_str}. Should be YYYY-MM-DD.")
        return None

class ToDoList:
    def __init__(self, data_file='tasks.json'):
        self.tasks = []
        self.data_file = data_file
        self.load_tasks()

    def add_task(self, description, priority, due_date):
        task = Task(description, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, task_id):
        if 0 <= task_id < len(self.tasks):
            del self.tasks[task_id]
            self.save_tasks()

    def mark_task_completed(self, task_id):
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id].completed = True
            self.save_tasks()

    def list_tasks(self):
        return self.tasks

    def save_tasks(self):
        with open(self.data_file, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    def load_tasks(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                tasks_data = json.load(f)
                self.tasks = [Task(**data) for data in tasks_data]

def format_task(task, index):
    due_date = task.due_date.strftime('%Y-%m-%d') if task.due_date else 'None'
    return f"{index}. [{task.priority.upper()}] {task.description} - Due: {due_date} - {'Completed' if task.completed else 'Pending'}"

def print_menu():
    print("\nTo-Do List Application")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Mark Task as Completed")
    print("4. List Tasks")
    print("5. Exit")

def get_due_date():
    due_date_str = input("Enter due date (YYYY-MM-DD) or leave blank: ")
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            return due_date
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
    return None

def main():
    todo_list = ToDoList()

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            description = input("Enter task description: ")
            priority = input("Enter task priority (low, mid, high): ").lower()
            due_date = get_due_date()
            todo_list.add_task(description, priority, due_date)
        elif choice == '2':
            task_id = int(input("Enter task ID to remove: "))
            todo_list.remove_task(task_id)
        elif choice == '3':
            task_id = int(input("Enter task ID to mark as completed: "))
            todo_list.mark_task_completed(task_id)
        elif choice == '4':
            tasks = todo_list.list_tasks()
            print("Tasks:")
            for index, task in enumerate(tasks):
                print(format_task(task, index))
        elif choice == '5':
            print("Exiting the to-do list application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
