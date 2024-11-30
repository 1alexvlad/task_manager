from datetime import date, datetime
from task import Task
import json


class TaskManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.tasks = [] 
        self.load_tasks()

    def load_tasks(self):
        """Загрузка задач из файла."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                tasks_data = json.load(file)
                self.tasks = []
                for task in tasks_data:
                    task['due_date'] = datetime.strptime(task['due_date'], '%Y-%m-%d').date() 
                    self.tasks.append(Task(**task)) 
        except FileNotFoundError:
            print('Файл не найден. Инициализация пустого списка задач.')
            self.tasks = [] 
        except json.JSONDecodeError:
            print("Ошибка: Неверный формат данных в файле. Инициализация пустого списка задач.")
            self.tasks = []  


    def tasks_views(self):
        """Просмотр всех задач"""
        
        if not self.tasks:
            print('Нет текущих задач')
            return 

        tasks_data = []
        for task in self.tasks:
            tasks_data.append(
                {
                   "ID": task.id,
                    "Название": task.title,
                    "Описание": task.description,
                    "Категория": task.category,
                    "Срок выполнения": task.due_date.isoformat(),
                    "Приоритет": task.priority,
                    "Статус": task.status 
                }
            )
        json_output = json.dumps(tasks_data, ensure_ascii=False, indent=4)
    
        print(json_output)


    def tasks_views_category(self, category: str):
        """Просмотр задач по категориям в формате JSON."""
        
        found_tasks = []

        for task in self.tasks:
            if category.lower() == task.category.lower():
                found_tasks.append({
                    "ID": task.id,
                    "Название": task.title,
                    "Описание": task.description,
                    "Категория": task.category,
                    "Срок выполнения": task.due_date,
                    "Приоритет": task.priority,
                    "Статус": task.status
                })

        if found_tasks:
            print('Найдены совпадения по категориям:')
            json_output = json.dumps(found_tasks, ensure_ascii=False, indent=4)
            print(json_output)  
        else:
            print('Категории не найдены')

    def task_add(self, title: str, description: str, category: str, due_date: date, priority: str, status: str):
        """Добавление новой задачи."""
        if priority not in ["Низкий", "Средний", "Высокий"]:
            print("Ошибка: Приоритет должен быть 'Низкий', 'Средний' или 'Высокий'.")
    
        try:
            due_date_obj = datetime.strptime(due_date, '%Y-%m-%d').date() 
            if due_date_obj < date.today():
                print("Ошибка: Срок выполнения не может быть меньше сегодняшней даты.")
                return
        except ValueError:
            print("Ошибка: Неверный формат даты. Используйте формат ГГГГ-ММ-ДД.")
            return

        task_id = len(self.tasks) + 1 
        new_task = Task(task_id, title, description, category, due_date_obj, priority, status)  
        self.tasks.append(new_task) 
        self.task_save()

    def task_save(self):
        """Сохранение задач в файл"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            task_to_save = [task.task_to_save_dict() for task in self.tasks]
            json.dump(task_to_save, file, ensure_ascii=False, indent=4)


    def task_change_status_is_done(self, task_id: int):
        """Отметка задачи как выполненной."""
        for task in self.tasks:
            if task_id == task.id:
                task.task_is_done()
                self.task_save()
                print(f'Задача с ID {task_id} отмечена как выполненная.')
                return
        
        print('Задача не найдена')

    def task_edit(self, task_id: int):
        """Редактирование существующей задачи."""
        for task in self.tasks:
            if task.id == task_id:
                print(f'Редактирование задачи с ID {task_id}:')
                
                title = input(f'Введите новое название (текущая: "{task.title}", оставить пустым для пропуска): ')
                if title:
                    task.title = title
                
                description = input(f'Введите новое описание (текущая: "{task.description}", оставить пустым для пропуска): ')
                if description:
                    task.description = description
                
                category = input(f'Введите новую категорию (текущая: "{task.category}", оставить пустым для пропуска): ')
                if category:
                    task.category = category
                
                due_date = input(f'Введите новый срок выполнения (текущий: "{task.due_date}", оставить пустым для пропуска): ')
                if due_date:
                    try:
                        due_date_obj = datetime.strptime(due_date, '%Y-%m-%d').date()
                        if due_date_obj < date.today():
                            print("Ошибка: Срок выполнения не может быть меньше сегодняшней даты.")
                            return
                        task.due_date = due_date_obj
                    except ValueError:
                        print("Ошибка: Неверный формат даты. Используйте формат ГГГГ-ММ-ДД.")
                    return

                
                priority = input(f'Введите новый приоритет (текущий: "{task.priority}", оставить пустым для пропуска): ')
                if priority in ['Низкий', 'Средний', 'Высокий']:
                    task.priority = priority
                else:
                    print("Ошибка: Приоритет должен быть 'Низкий', 'Средний' или 'Высокий'.")
                
                status = input(f'Введите новый приоритет (текущий: "{task.status}", оставить пустым для пропуска): ')
                if status in ["Не выполнена", "Выполнена"]:
                    task.status = status
                
                self.task_save()
                print(f'Задача с ID {task_id} успешно обновлена.')
                return
        
        print('Задача не найдена.')


    def task_delete(self, task_id: int = None, category: str = None):
        """Удаление задачи"""
        count = len(self.tasks)
        self.tasks = [task for task in self.tasks if (task_id is None or task.id != task_id) and 
                  (category is None or task.category != category)]

        self.task_save()

        if len(self.tasks) < count:
            print('Задачи успешно удалены')
        print('Задачи не найдены')


    def task_search(self, keyword: str, category: str = None, status: str = None):
        """Поиск задач по ключевым словам, категории или статусу выполнения."""
        find_tasks = []

        for task in self.tasks:
            keyword_match = (keyword and (keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()))
            
            category_match = (category and category.lower() == task.category.lower())
            status_match = (status and status.lower() == task.status.lower())

            if keyword_match or category_match or status_match:
                find_tasks.append({
                    "ID": task.id,
                    "Название": task.title,
                    "Описание": task.description,
                    "Категория": task.category,
                    "Срок выполнения": task.due_date,
                    "Приоритет": task.priority,
                    "Статус": task.status
                })

            if find_tasks:
                print('Найденные задачи:')
                json_output = json.dumps(find_tasks, ensure_ascii=False, indent=4)
                print(json_output) 
            else:
                print('Задачи не найдены')