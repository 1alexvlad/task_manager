import pytest
import json
import os
from task_manager import TaskManager

@pytest.fixture
def create_temp_file():
    file_path = "tasks.json"
    tasks_data = [
        {
            'id': 1,
            'title': 'Задача 1',
            'description': 'Описание 1',
            'category': 'Категория 1',
            'due_date': '2023-12-31',
            'priority': 'Высокий',
            'status': 'Не выполнена'
        },
        {
            'id': 2,
            'title': 'Задача 2',
            'description': 'Описание 2',
            'category': 'Категория 2',
            'due_date': '2024-01-01',
            'priority': 'Средний',
            'status': 'Не выполнена'
        }
    ]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(tasks_data, f, ensure_ascii=False, indent=4)
        
    yield file_path
    
    if os.path.exists(file_path):
        os.remove(file_path)

class TestTaskManager:

    def test_load_tasks(self, create_temp_file):
        """Проверяет загрузку задач из файла"""
        manager = TaskManager(create_temp_file)
        
        assert len(manager.tasks) == 2
        assert manager.tasks[0].title == 'Задача 1'
        assert manager.tasks[1].title == 'Задача 2'

    def test_load_tasks_file_not_found(self):
        """Проверяет обработку отсутствующего файла"""
        manager = TaskManager("файл_не_найден.json")
        
        assert len(manager.tasks) == 0

    def test_load_tasks_invalid_json(self, tmp_path):
        """Проверяет обработку неверного формата JSON"""
        invalid_file = tmp_path / "недопустимые_задачи.json"
        with open(invalid_file, 'w', encoding='utf-8') as f:
            f.write("недопустимый json")
        
        manager = TaskManager(str(invalid_file))
        
        assert len(manager.tasks) == 0

    def test_task_add(self, create_temp_file):
        """Проверяет добавление новой задачи"""
        manager = TaskManager(create_temp_file)
        manager.task_add("Новая задача", "Новое описание", "Новая категория", "2024-12-15", "Низкий", "Не выполнена")
        
        assert len(manager.tasks) == 3
        assert manager.tasks[2].title == "Новая задача"

    def test_task_add_due_date_in_past(self, create_temp_file):
        """Проверяет добавление задачи с датой выполнения в прошлом (должно игнорироваться)."""
        manager = TaskManager(create_temp_file)
        manager.task_add("Старая задача", "Старое описание", "Старая категория", "2000-01-01", "Низкий", "Не выполнена")
        
        assert len(manager.tasks) == 2

    def test_task_views(self, temp_file, output_capture):
        """Проверяет вывод всех задач"""
        task_manager = TaskManager(temp_file)  
        task_manager.tasks_views()
        
        captured_output = output_capture.readouterr() 
        
        assert 'Задача 1' in captured_output.out
        assert 'Задача 2' in captured_output.out

    def test_task_views_category_not_found(self, temp_file, output_capture):
        """Проверяет вывод при отсутствии задач в заданной категории."""
        task_manager = TaskManager(temp_file) 
        task_manager.tasks_views_category("Несуществующая категория")
        
        captured_output = output_capture.readouterr()
        
        assert 'Категории не найдены' in captured_output.out