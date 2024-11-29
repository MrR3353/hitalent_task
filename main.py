import datetime

from task import TaskPriority, TaskStatus
from task_manager import TaskManager


def main():
    manager = TaskManager('tasks.json')

    while True:
        print("\nМеню:")
        print("1. Просмотр задач")
        print("2. Добавление задачи")
        print("3. Изменение задачи")
        print("4. Удаление задачи")
        print("5. Поиск задач")
        print("6. Выйти")

        choice = input("Выберите действие: ")
        if choice == "1":
            category = input("Введите категорию (или оставьте пустым): ")
            tasks = manager.get_tasks(category)
            if tasks:
                for task in tasks:
                    print(task.to_dict())
            else:
                print("Задачи не найдены")
        elif choice == "2":
            title = input("Название: ")
            description = input("Описание: ")
            category = input("Категория: ")
            due_date = input("Срок выполнения (в формате YYYY-MM-DDTHH:MM:SS): ")
            try:
                due_date = datetime.datetime.fromisoformat(due_date)
            except ValueError:
                print("Неверное значение. Используйте формат YYYY-MM-DDTHH:MM:SS, например 2024-12-01T00:00:00.")
                continue
            priority = input("Приоритет (" + ", ".join([p.value for p in TaskPriority]) + "): ")
            try:
                priority = TaskPriority(priority)
            except ValueError:
                print(f"Неверное значение. Допустимые значения: {', '.join([p.value for p in TaskPriority])}")
                continue
            status = input("Статус (" + ", ".join([s.value for s in TaskStatus]) + "): ")
            try:
                status = TaskStatus(status)
            except ValueError:
                print(f"Неверное значение. Допустимые значения: {', '.join([s.value for s in TaskStatus])}")
                continue
            manager.add_task(title, description, category, due_date, priority, status)
            print("Задача добавлена успешно!")
        elif choice == "3":
            try:
                task_id = int(input("Введите ID задачи: "))
                print("Оставьте поле пустым, если не хотите его изменять.")
                title = input("Новое название: ")
                description = input("Новое описание: ")
                category = input("Новая категория: ")
                due_date = input("Новый срок выполнения (в формате YYYY-MM-DDTHH:MM:SS): ")
                try:
                    if due_date:
                        due_date = datetime.datetime.fromisoformat(due_date)
                    else:
                        due_date = None
                except ValueError:
                    print("Неверное значение. Используйте формат YYYY-MM-DDTHH:MM:SS, например 2024-12-01T00:00:00.")
                    continue

                priority = input("Новый приоритет (" + ", ".join([p.value for p in TaskPriority]) + "): ")
                try:
                    if priority:
                        priority = TaskPriority(priority)
                    else:
                        priority = None
                except ValueError:
                    print(f"Неверное значение. Допустимые значения: {', '.join([p.value for p in TaskPriority])}")
                    continue
                status = input("Новый статус (" + ", ".join([s.value for s in TaskStatus]) + "): ")
                try:
                    if status:
                        status = TaskStatus(status)
                    else:
                        status = None
                except ValueError:
                    print(f"Неверное значение. Допустимые значения: {', '.join([s.value for s in TaskStatus])}")
                    continue

                manager.edit_task(task_id, title=title, description=description, category=category, 
                                  due_date=due_date, priority=priority, status=status)
                print("Задача обновлена успешно!")
            except ValueError as e:
                print(f"Ошибка: {e}")
        elif choice == "4":
            try:
                task_id = int(input("Введите ID задачи: "))
                manager.delete_task(task_id)
                print("Задача удалена успешно!")
            except ValueError:
                print("Ошибка: Некорректный ID.")
        elif choice == "5":
            print("Оставьте поле пустым, если не хотите выполнять поиск по нему")
            keyword = input("Введите ключевое слово: ")
            category = input("Категория: ") or None
            status = input("Статус (" + ", ".join([s.value for s in TaskStatus]) + "): ")
            try:
                if status:
                    status = TaskStatus(status)
                else:
                    status = None
            except ValueError:
                print(f"Неверное значение. Допустимые значения: {', '.join([s.value for s in TaskStatus])}")
                continue
            tasks = manager.search_tasks(keyword, category, status)
            if tasks:
                for task in tasks:
                    print(task.to_dict())
            else:
                print("Задачи не найдены")
        elif choice == "6":
            break
        else:
            print("Неверный выбор, попробуйте снова.")


main()