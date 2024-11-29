import datetime
import os

import pytest
from task_manager import TaskManager
from task import TaskPriority, TaskStatus

task_data = {"title": "Test Task",
             "description": "Description",
             "category": "Test",
             "due_date": datetime.datetime(2024, 12, 10, 6, 0, 0),
             "priority": TaskPriority.HIGH,
             "status": TaskStatus.NOT_COMPLETED}

test_filename = "test_tasks.json"


@pytest.fixture(autouse=True)
def cleanup():
    # Код перед тестом (если нужен)
    yield  # Точка, где выполняется сам тест
    # Код после теста
    os.remove(test_filename)


def test_add_task():
    manager = TaskManager(test_filename)
    manager.add_task(**task_data)
    assert len(manager.tasks) == 1
    results = manager.get_tasks()
    assert len(results) == 1
    assert results[0].title == task_data['title']
    assert results[0].description == task_data['description']
    assert results[0].category == task_data['category']
    assert results[0].due_date == task_data['due_date']
    assert results[0].priority == task_data['priority']
    assert results[0].status == task_data['status']


def test_edit_task():
    manager = TaskManager(test_filename)
    manager.add_task(**task_data)
    manager.edit_task(1, "Updated Task", None, None, None, None, TaskStatus.COMPLETED)
    assert manager.tasks[0].title == "Updated Task"


def test_delete_task():
    manager = TaskManager(test_filename)
    manager.add_task(**task_data)
    assert len(manager.tasks) == 1
    manager.delete_task(1)
    assert len(manager.tasks) == 0


def test_search_task():
    manager = TaskManager(test_filename)
    manager.add_task(**task_data)
    results = manager.search_tasks("Test")
    assert len(results) == 1
    assert results[0].title == task_data['title']
    assert results[0].description == task_data['description']
    assert results[0].category == task_data['category']
    assert results[0].due_date == task_data['due_date']
    assert results[0].priority == task_data['priority']
    assert results[0].status == task_data['status']
