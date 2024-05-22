from validations import is_only_chars, is_phone, is_uuid, is_date, is_address

def body_parser(func):
  def inner(*args):
    try:
      cmd, *payload = args[0].split(" ")

      return func(cmd.lower(), payload)
    except ValueError:
      print("Give me name and phone please.")

  return inner

def add_user_validation(func):
  def inner(*args, **kwargs):
    try:
      payload = args[0]

      if not is_only_chars(payload[0]):
        raise ValueError
      
      if not is_phone(payload[1]):
        raise ValueError
          
      return func(*args, **kwargs)
    except ValueError:
      print("Give me valid name(only chars) and phone(start with +380) please.")

  return inner

def edit_user_by_id_validation(func):
  def inner(*args, **kwargs):
    try:
      payload = args[0]

      if not is_uuid(payload[0]):
        raise ValueError
      
      if not is_only_chars(payload[1]):
        raise ValueError
      
      if not is_phone(payload[2]):
        raise ValueError

      return func(*args, **kwargs)
    except ValueError:
      print("Give me valid user id(should be UUID) and new name(only chars) and phone(start with +380) please.")

  return inner

def get_phone_validation(func):
  def inner(*args, **kwargs):
    try:
      payload = args[0]

      if not is_only_chars(payload[0]):
        raise ValueError

      return func(*args, **kwargs)
    except ValueError:
      print("Give me valid  name(only chars).")

  return inner

def add_birthday_validation(func):
  def inner(*args, **kwargs):
    try:
      payload = args[0]

      if not is_uuid(payload[0]):
        raise ValueError
      
      if not is_date(payload[1]):
        raise ValueError

      return func(*args, **kwargs)
    except ValueError:
      print("Give me valid id(UUID) and date(YYYY.MM.DD) please.")

  return inner

def show_birthday_validation(func):
  def inner(*args, **kwargs):
    try:
      payload = args[0]

      if not is_only_chars(payload[0]):
        raise ValueError

      return func(*args, **kwargs)
    except ValueError:
      print("Give me valid id(UUID) and date(YYYY.MM.DD) please.")

  return inner

def add_address_validation(func):                         # A-1 Доданий декоратор
  def inner(*args, **kwargs):
    try:
      payload = args[0]

      if not is_address(payload[0]):
        raise ValueError

      return func(*args, **kwargs)
    except ValueError:
      print("Give me a valid address.Example->->-> Country: Ukraine, City: Kiyv, Street: Hreschatyk, House Number: 45, Apartment Number: 1")

  return inner

