import sys

from decorators import body_parser, add_user_validation, edit_user_by_id_validation, get_phone_validation, add_birthday_validation, show_birthday_validation
from storage import add_user_to_store, find_all_users_from_store, update_user_by_id, get_user_phone_by_name, add_birthday_to_user, get_birthday_by_name, get_birthdays

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
List app commands:
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
  result = update_user_by_id(id, new_name, new_phone)

  if result:
    print("\nUser data updated!\n")
  else:
    print("\nUser not found!\n")

@get_phone_validation
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
  }
}