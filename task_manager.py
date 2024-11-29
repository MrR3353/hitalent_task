import json
from typing import List, Optional
import datetime

from task import Task, TaskPriority, TaskStatus


class TaskManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.tasks: List[Task] = self.load_tasks()

    def load_tasks(self) -> List[Task]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [
                    Task.from_dict(task) for task in data
                ]
        except FileNotFoundError:
            print(f'Файл {self.file_path} не найден')
            return []
        except Exception as e:
            print(f'Ошибка чтения {e} в {self.file_path}')
            return []

    def save_tasks(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4, ensure_ascii=False)

    def add_task(self, title: str, description: str, category: str,
                 due_date: datetime.datetime, priority: TaskPriority, status: TaskStatus):
        task_id = max((task.id for task in self.tasks), default=0) + 1
        new_task = Task(task_id, title, description, category, due_date, priority, status)
        self.tasks.append(new_task)
        self.save_tasks()

    def edit_task(self, task_id: int, title: str, description: str, category: str,
                  due_date: datetime.datetime, priority: TaskPriority, status: TaskStatus):
        task = self.find_task_by_id(task_id)
        if not task:
            raise ValueError("Задача с таким ID не найдена.")
        if title:
            task.title = title
        if description:
            task.description = description
        if category:
            task.category = category
        if due_date:
            task.due_date = due_date
        if priority:
            task.priority = priority
        if status:
            task.status = status
        self.save_tasks()

    def delete_task(self, task_id: int):
        tasks = [task for task in self.tasks if task.id != task_id]
        if len(self.tasks) == tasks:
            raise ValueError(f'{task_id} не существует')
        else:
            self.tasks = tasks
            self.save_tasks()

    def find_task_by_id(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def search_tasks(self, keyword: str = "", category: str = "", status: TaskStatus = None) -> List[Task]:
        return [
            task for task in self.tasks
            if (keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()) and
               (not category or task.category.lower() == category.lower()) and
               (not status or task.status.value == status.value)
        ]

    def get_tasks(self, category: str = "") -> List[Task]:
        if category:
            return [task for task in self.tasks if task.category.lower() == category.lower()]
        return self.tasks
