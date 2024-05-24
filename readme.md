# project-group-2

Опис роботи застосунку контактів

## Запуск

```bash
python cli.py
```

## Використання

Після запуску команди виводиться інтерфейс

```bash
Start typing the command: # Інпут команди

# Cписок всіх команд
=> Add Contact # Теперішня команда, яку намагається вгадати термінал
Edit Contact 
Remove Contact
Get Contact by Id
Get Contact by Name
Get Contact by Phone
List Contacts
Edit Birthday
Edit Address
Edit Plate
Edit Email
Get Greetin Days
Add Note
Edit Note
Remove Note
Get Note by Id
List Tags
Get Notes by Tag
Get Notes by Text
List Notes
```
При вводі команди інтерфейс намагається вгадати, яку команду ви хочете використати

```bash
Start typing the command: edi # початок назви команди

# список команд
=> Edit Contact # Теперішня команда, яку намагається вгадати термінал
Edit Birthday
Edit Address
Edit Plate
Edit Email
Edit Note
```
Якщо натиснути на 'Enter', то виконається команда 'Edit Contact'

```bash
--------------Edit Contact--------------

Enter Id: # Полу вводу даних
```
