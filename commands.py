import sys

from decorators import body_parser, add_user_validation, edit_user_by_id_validation,\
  phone_validation, add_birthday_validation, show_birthday_validation,\
    add_car_number_validation, name_validation, add_email_validation,\
    uuid_validation, add_note_validation, update_note_validation, show_notes_by_tag_validation,\
    search_notes_validation, add_address_validation
from storage import add_user_to_store, find_all_users_from_store, update_user_by_id,\
  get_user_phone_by_name, add_birthday_to_user, get_birthday_by_name, get_birthdays,\
    add_car_number_to_user, delete_user_by_id,  get_contact_by_name, get_contact_by_phone, add_email_to_user,\
    add_new_note, find_all_notes, find_all_tags, update_note_by_id, get_notes_by_tag, find_note_by_id,\
    search_notes_by_substring, delete_note_by_id, add_address_by_id, edit_address_by_id
from helper import args_to_string_parser

@body_parser
def run(cmd: str, payload):
  try:
    if len(payload) > 0:
      handler = commands[cmd].get("handler")
      handler(payload)
    else:
      handler = commands[cmd].get("handler")
      handler()
  except:
    if cmd == "exit" or cmd == "close":
      sys.exit(0)
    else:
      print("\nCommand not found!\n")

def help_app():
  help_str =f"""
List address book commands:
  1. "~$/help" - show command list
  2. "~$/exit" or "~$/close" - exit from app
  3. "~$/hello" - print hello message
  4. "~$/add_user [name<str>] [phone<str>]" - create new user and return entity
  5. "~$/show_all_users" - show all users in store
  6. "~$/update_user [id<UUID>] [name<str>] [phone<str>]" - update user by id
  7. "~$/get_phone [name<str>]" - get phone by user name
  8. "~$/add_birthday [id<UUID>] [date<Date>]" - add birthday to user. date format: "YYYY.MM.DD"
  9. "~$/show_birthday [name<str>]" - show birthday by name
  10."~$/birthdays" - show all upcoming birthdays
  11."~$/delete [id<UUID>]
  12."~$/add_car_number [id<UUID>] [number<str>]" - add user's car license plate number ex: AA 1234 BB
  13."~$/find_contact_by_name [name<str>]" - find contact by name
  14."~$/find_contact_by_phone [phone<str>]" - find contact by phone
  15."~$/add_email [id<UUID>] [adress<str>]" - add email to user. email format: "xxx@xx.xx"
  16."~$/add_address [id<UUID>] [country<str>] [city<str>] [street<str>] [building<str>] [appartment<str>] (optional) )" - added new address to contacts. Ex. Ukraine Kyiv Hreschatyk 45 4
  17."~$/edit_address [id<UUID>] [country<str>] [city<str>] [street<str>] [building<str>] [appartment<str>] (optional) )" - added new address to contacts. Ex. Ukraine Kyiv Hreschatyk 45 4

Notes commands:
  1. "~$/add_note [note<str>]" - add note. [note<str>] = "note text #tag1 #tag2"
  2. "~$/show_all_notes" - show all notes
  3. "~$/show_all_tags" - show all tags
  4. "~$/update_note [id<UUID>] [note<str>]" - update note by id
  5. "~$/show_notes_by_tag [tag<str>]" - show notes by tag
  6. "~$/show_note [id<UUID>]" - show note by id
  7. "~$/search_notes [substring<str>]" - search notes by substring
"""
  print(help_str)

def hello():
  print("How can I help you?\n")

def exit_from_app():
  print("Good bye!")
  sys.exit(0)

@add_user_validation
def add_user(payload):
  name = payload[0]
  phone = payload[1]
  new_user = add_user_to_store(name, phone)
  print(f"\nUser added!\nEntity:\n{new_user}\n")

def show_all_users():
  users = find_all_users_from_store()
  print("\nUsers:");
  for user in users:
    print(f"{user}")
  print("\n")

@edit_user_by_id_validation
def edit_user_by_id(payload):
  id = payload[0]
  new_name = payload[1]
  new_phone = payload[2]
  new_birthday = payload[3] if len(payload) > 3 else None
  result = update_user_by_id(id, new_name, new_phone, new_birthday)

  if result:
    print("\nUser data updated!\n")
  else:
    print("\nUser not found!\n")

@phone_validation
def get_phone(payload):
  name = payload[0]
  phone = get_user_phone_by_name(name)  

  if phone:
    print(f"\nPhone: {phone}\n")

@add_birthday_validation
def add_birthday(payload):
  id = payload[0]
  date = payload[1]
  result = add_birthday_to_user(id, date)

  if result:
    print(f"\nBirthday successfuly added\n")
  else:
    print(f"\nError: birthday is not added\n")

@ add_email_validation
def add_email(payload):
  id = payload[0]
  email = payload[1]
  result = add_email_to_user(id, email)
  if result:
    print(f"\nEmail successfuly added\n")
  else:
    print(f"\nError: Email is not added\n")

@show_birthday_validation
def show_birthday(payload):
  name = payload[0]

  birthday = get_birthday_by_name(name)

  if birthday:
    print(f"\nBirthday {name} is {birthday}\n")
  else:
    print(f"\nError: birthday is not found\n")

def birthdays():
  result = get_birthdays();

  for item in result:
    print(f"{item["name"]}: {item["congratulation_date"]}\n")

@uuid_validation
def delete_user(payload):
   id = payload[0]
   message = delete_user_by_id(id)
   print(f"{message}")

@add_car_number_validation
def add_car_number(payload):
  id = payload[0]
  number = payload[1]
  result = add_car_number_to_user(id, number)

  if result:
    print(f"\nCar number successfuly added\n")
  else:
    print(f"\nError: car number is not added\n")


@name_validation
def find_contact_by_name(payload):
 name: str = payload[0]
 print(get_contact_by_name(name))


@phone_validation
def find_contact_by_phone(payload):
  phone: str = payload[0]
  print(get_contact_by_phone(phone))

@add_address_validation                 # A-1  Додано додавання адреси, виправлено на is_address на add_addresss, додані параметри id та address
def add_address(payload):
    id = payload[0]
    address = {
      "country": payload[1],
      "city": payload[2],
      "street": payload[3],
      "house_number": payload[4],
      "apartment_number": payload[5] if len(payload) > 5 else None
    }

    if add_address_by_id(id, address):
        print("Address added successfully!")
    else:
        print("Invalid address format!")

@add_address_validation
def edit_address(payload):
  id = payload[0]
  address = {
    "Country": payload[1],
    "City": payload[2],
    "Street": payload[3],
    "House Number": payload[4],
    "Apartment Number": payload[5] if len(payload) > 5 else None
  }

  if edit_address_by_id(id, address):
      print("Address updated successfully!")
  else:
      print("Invalid updated format!")

#########################
# Notes commands
#########################

@add_note_validation
def add_note(payload):
  data = args_to_string_parser(payload)
  res = add_new_note(data)

  if res["result"]:
    if len(res["tags"]) > 0:
      print(f"\nNote with id '{res["note"]["id"]}' added with tags: {res["tags"]}\n")
    else:
      print("\nNote added\n")

def show_all_notes():
  print("\nNotes:")
  notes = find_all_notes()
  index = 1
  for note in notes:
    print(f"{index}. Id: {note.get_id()}. Note: \"{note.get_text()}\"")
    index += 1
  print("\n")

def show_all_tags():
  print("\nTags:")
  tags = find_all_tags()
  for tag in tags:
    print(f"#{tag}")
  print("\n")

@update_note_validation
def update_note(payload):
  id = payload[0]
  new_text = args_to_string_parser(payload[1:])
  res = update_note_by_id(id, new_text)

  if res:
    print("\nNote updated\n")
  else:
    print("\nNote not found\n")

@show_notes_by_tag_validation
def show_notes_by_tag(payload):
  tag = payload[0].split("#")[1]
  notes = get_notes_by_tag(tag)

  if notes and len(notes) > 0:
    index = 1
    for note in notes:
      print(f"{index}. Id: {note.get_id()}. Note: \"{note.get_text()}\"")
      index += 1
    print("\n")
  else:
    print("\nNotes not found\n")

@uuid_validation
def show_note(payload):
  id = payload[0]
  note = find_note_by_id(id)

  if note:
    print(f"\nId: {note.get_id()}. Note: \"{note.get_text()}\"\n")
  else:
    print("\nNote not found\n")

@search_notes_validation
def search_notes(payload):
  substring = payload[0]
  notes = search_notes_by_substring(substring)

  if notes and len(notes) > 0:
    index = 1
    for note in notes:
      print(f"{index}. Id: {note.get_id()}. Note: \"{note.get_text()}\"")
      index += 1
    print("\n")
  else:
    print("\nNotes not found\n")

@uuid_validation
def delete_note(payload):
  id = payload[0]
  res = delete_note_by_id(id)

  if res:
    print("\nNote deleted\n")
  else:
    print("\nNote not found\n")


commands = {
  "help": {
    "handler": help_app,
  },
  "exit":{
    "handler": exit_from_app,
  },
  "close":{
    "handler": exit_from_app,
  },
  "hello":{
    "handler": hello,
  },
  "add_user":{
    "handler": add_user,
  },
  "show_all_users":{
    "handler": show_all_users,
  },
  "update_user":{
    "handler": edit_user_by_id,
  },
  "get_phone":{
    "handler": get_phone 
  },
  "add_birthday": {
    "handler": add_birthday
  },
  "show_birthday": {
    "handler": show_birthday
  },
  "birthdays": {
    "handler": birthdays
  },
  "add_address": {
    "handler": add_address                      # A-1  Додано додавання адреси
  },
  "edit_address": {
    "handler": edit_address
  },
  "delete": {
    "handler": delete_user
  },
  "add_car_number": {
    "handler": add_car_number
  },
    "find_contact_by_name": {
    "handler": find_contact_by_name
  },
    "find_contact_by_phone": {
    "handler": find_contact_by_phone
  },
    "add_email": {
    "handler": add_email
  },

  #########################
  # Notes commands
  #########################
  "add_note": {
    "handler": add_note
  },
  "show_all_notes": {
    "handler": show_all_notes
  },
  "show_all_tags": {
    "handler": show_all_tags
  },
  "update_note": {
    "handler": update_note
  },
  "show_notes_by_tag": {
    "handler": show_notes_by_tag
  },
  "show_note": {
    "handler": show_note
  },
  "search_notes": {
    "handler": search_notes
  },
  "delete_note": {
    "handler": delete_note
  }
}