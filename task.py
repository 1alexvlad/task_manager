

from datetime import date


class Task:
    def __init__(self, id: int, title: str, description: str, category: str, due_date: date, priority: str, status: str):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = 'Не выполнена'


    def task_is_done(self):
        self.status = 'Выполнена' 

    
    def task_to_save_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'due_date': self.due_date.isoformat(),
            'priority': self.priority,
            'status': self.status
        }