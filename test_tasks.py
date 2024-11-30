from datetime import date
from task import Task

def test_task_creation():
    """Проверяет создание задачи"""
    task = Task(1, "Тест", "Описание для теста", "Тестовая категория", date(2023, 12, 31), "Высокий", "Не выполнена")
    
    assert task.id == 1
    assert task.title == "Тест"
    assert task.description == "Описание для теста"
    assert task.category == "Тестовая категория"
    assert task.due_date == date(2023, 12, 31)
    assert task.priority == "Высокий"
    assert task.status == "Не выполнена"

def test_task_is_done():
    """Проверяет изменение статуса задачи на "Выполнена"""
    task = Task(1, "Тест", "Описание для теста", "Тестовая категория", date(2023, 12, 31), "Высокий", "Не выполнена")
    task.task_is_done()
    
    assert task.status == "Выполнена"

def test_task_to_save_dict():
    """ПровПроверяет корректность преобразования задачи в словарь"""
    task = Task(1, "Тестовая задача", "Это тестовая задача", "Тестовая категория", date(2023, 12, 31), "Высокий", "Не выполнена")
    expected_dict = {
        'id': 1,
        'title': "Тестовая задача",
        'description': "Это тестовая задача",
        'category': "Тестовая категория",
        'due_date': "2023-12-31",
        'priority': "Высокий",
        'status': "Не выполнена"
    }
    
    assert task.task_to_save_dict() == expected_dict