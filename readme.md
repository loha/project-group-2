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

## Команди

Команда: Add Contact - Додавання контакту

Етапи:

1. Вписуємо потрібну команду 
```bash
Start typing the command: add # Натискаємо на Enter

=> 1. Add Contact
10. Edit Address
14. Add Note
```

2. Заповнюємо поле Name та Phone. Кожне поле валідується. Якщо все введено правильно, то контакт створюється
```bash
-------------1. Add Contact-------------

Enter Name: Armen
Enter Phone: +380962343322

------Contact successfully created------

{'id': e9118b02-82a2-4cc6-a13d-c3bea8215aaa, 'name': Armen, 'phone': +380962343322, 'birthday': None, 'address': None, 'email': None, 'plate': None}
Press any key to continue
```


Команда: Edit Plate - Редагування номеру автомобіля 

Етапи:

1. 1. Вписуємо потрібну команду 
```bash
Start typing the command: edit P # Натискаємо на Enter

=> 12. Edit Plate
```

2. Вписуємо айді контакту, який хочемо редагувати. Потім вписуємо номер автомобіля і виводиться результат
```bash
-------------12. Edit Plate-------------

Enter Id: e9118b02-82a2-4cc6-a13d-c3bea8215aaa

{'id': e9118b02-82a2-4cc6-a13d-c3bea8215aaa, 'name': Armen, 'phone': +380962343322, 'birthday': None, 'address': None, 'email': None, 'plate': None}
Enter Plate: AH8597
Plate must have from 3 to 7 alphanums
-------Plate updated successfully-------

{'id': e9118b02-82a2-4cc6-a13d-c3bea8215aaa, 'name': Armen, 'phone': +380962343322, 'birthday': None, 'address': None, 'email': None, 'plate': AH8597}
Press any key to continue
```

Команда: Get Contact by Plate - Пошук контакта по номеру автомобіля

Етапи:

1. Вписуємо потрібну команду

```bash
Start typing the command: get contact by pl # Натискаємо на Enter

=> 7. Get Contact by Plate
```

2. Вписуємо номер автомобіля. Якщо такий номер є, то контакт виводиться

```bash
--------7. Get Contact by Plate---------

Enter Plate: AH8597

-------------Contact found--------------

{'id': e9118b02-82a2-4cc6-a13d-c3bea8215aaa, 'name': Armen, 'phone': +380962343322, 'birthday': None, 'address': None, 'email': None, 'plate': AH8597}
Press any key to continue
```


Команда: Add Note - Додавання нотатки

Етапи:

1. Вписуємо потрібну команду
```bash
Start typing the command: add no # Натискаємо на Enter

=> Add Note
```

2. Вписуємо нотатку в поле. В полі можна вписувати теги через символ '#' і теги автоматично розпарсяться і додадуться в окремий список. В цьому прикладі додався тег '#Lamborghini'
```bash
----------------Add Note----------------

Enter Note: 2024.05.02 - Була викрадена Lamborghini diablo #Lamborghini       



------Contact successfully created------

Id: 8ada9a01-5523-41a2-9c41-5b91572e9132. Text: 2024.05.02 - Була викрадена Lamborghini diablo #Lamborghini

Press any key to continue
```

Команда: List Notes - Вивід списка нотаток

Етапи:

1. Вписуємо команду 
```bash
Start typing the command: list n # Натискаємо на Enter

=> List Notes
```

2. Виводиться список нотаток
```bash
---------------List Notes---------------

Id: 60369311-70a2-4a02-a582-a604b8d57280. Text: alksdlfmalsd dsa #tag2
Id: a1b57ad6-e3b3-4600-b7d6-4871dfa1f957. Text: alksdnflaknsdl sdf #tag1
Id: 2c9969b3-dbd7-4770-a290-db70ae54dc94. Text: alksdjflkjsdf #tag1
Id: 41e89b74-19ff-4447-8560-82b78f8ab774. Text: alsdkjflkjdsf #tag2
Id: 8ada9a01-5523-41a2-9c41-5b91572e9132. Text: 2024.05.02 - Була викрадена Lamborghini diablo #Lamborghini

Press any key to continue
```

Команда: List Tags - Вивід списка тегів

Етапи:

1. Вписуємо команду 

```bash
Start typing the command: List t # Натискаємо на Enter

=> List Tags
```

2. Виводиться список тегів
```bash
---------------List Tags----------------

Lamborghini
tag1
tag2

Press any key to continue
```

Команда: Get Notes by Tag - вивід списку нотаток по тегу

1. Вписуємо команду
```bash
Start typing the command: Get Notes by Tag

=> Get Notes by Tag
```

2. Вписуємо назву тега
```bash
------------Get Notes by Tag------------

Enter Tag: Lamborghini
```

3. Виводиться список нотаток по тегу
```bash
Id: 8ada9a01-5523-41a2-9c41-5b91572e9132. Text: 2024.05.02 - Була викрадена Lamborghini diablo #Lamborghini

Press any key to continue
```

Інші команди нотаток:

1. Edit Note - Редагування нотатки. Потрібно ввести Id<UUID> нотатки і ввсести нове значення нотатки
2. Remove Note - Видалення нотатки. Потрібно ввести Id<UUID> нотатки для видалення
3. Get Note by Id - Отримання нотатки по Id. Потрібно ввести Id<UUID> нотатки для відображення конкретної нотатки
4. Get Notes by Text - Пошук нотаток. Потрібно ввести підстроку, яку потрібно знайти