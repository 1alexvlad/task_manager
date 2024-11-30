from task_manager import TaskManager


def main():
    manager = TaskManager('data.json')

    while True:
        print()
        print("1 Просмотреть задачи")
        print("2 Просмотр задач по категориям")
        print("3 Добавление новой задачи")
        print("4 Редактирование существующей задачи")
        print("5 Отметка задачи как выполненной.")
        print("6 Удаление задачи по идентификатору или категории")
        print("7 Поиск по ключевым словам, категории или статусу выполнения.")
        print("8 Выйти")

    
        result = int(input('Выберите номер действия: '))

        if result == 1:
            manager.tasks_views()

        elif result == 2:
            look_category = input('Введите категорию: ')
            manager.tasks_views_category(look_category)

        elif result == 3:
            title = input('Введите название: ')
            description = input("Введите описание: ")
            category = input("Введите категория: ")
            due_date = input("Срок выполнения (Год-Месяц-День): ")
            priority = input("Введите приоритет (Низкий, Средний, Высокий): ")
            status = input('Введите статус (Не выполнена/Выполнена): ')  
            manager.task_add(title, description, category, due_date, priority, status)


        elif result == 4:
            task_id = int(input('Введите id задачи для редактирование: '))
            manager.task_edit(task_id)


        elif result == 5:
            task_id = int(input('Введите id задачи для отметки как выполненной: '))
            manager.task_change_status_is_done(task_id)
        

        elif result == 6:
            task_id_input = input('Введите ID задачи для удаления (или оставьте пустым): ')
            category_input = input('Введите категорию для удаления (или оставьте пустым): ')

            task_id = int(task_id_input) if task_id_input.isdigit() else None
            category = category_input if category_input else None
            
            manager.task_delete(task_id, category)

        
        elif result == 7:
            keyword = input('Введите ключевое слово для поиска (или оставьте пустым): ') or None
            category = input('Введите категорию (или оставьте пустым): ') or None
            status = input('Введите статус (или оставьте пустым): ') or None
            manager.task_search(keyword, category, status)


        elif result == 8:
            print('Выход из программы')
            break
        
        else:
            print('Выберите номер от 1 до 8')

if __name__ == "__main__":
    main()