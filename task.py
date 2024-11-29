import datetime
from enum import Enum


class TaskStatus(Enum):
    NOT_COMPLETED = "Не выполнена"
    COMPLETED = "Выполнена"


class TaskPriority(Enum):
    LOW = "Низкий"
    MIDDLE = "Средний"
    HIGH = "Высокий"


class Task:
    def __init__(self, task_id: int, title: str, description: str, category: str,
                 due_date: datetime.datetime, priority: TaskPriority, status: TaskStatus = TaskStatus.NOT_COMPLETED):
        self.id = task_id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date.isoformat(),
            "priority": self.priority.value,
            "status": self.status.value
        }

    @staticmethod
    def from_dict(data: dict):
        return Task(
            task_id=data["id"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            due_date=datetime.datetime.fromisoformat(data["due_date"]),
            priority=TaskPriority(data["priority"]),
            status=TaskStatus(data["status"])
        )

