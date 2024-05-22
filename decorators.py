from validations import is_only_chars, is_phone, is_uuid, is_date, is_car_number

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

      if len(payload) > 3 and not is_date(payload[3]):
        raise ValueError

      return func(*args, **kwargs)
    except ValueError:
      print("Give me valid user id(should be UUID) or name(only chars) or" +
            " phone(start with +380) or birthday(YYYY.MM.DD) please.")

  return inner


def name_validation(func):
  def inner(payload):
      if not is_only_chars(payload[0]):
        print("Give me a valid name (has only chars)")

      return func(payload)
  return inner


def phone_validation(func):
  def inner(payload):
      if not is_phone(payload[0]):
        print("Give me a valid phone (has format +380XXXXXXXXX)")

      return func(payload)
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

def delete_users_validation(func):
  def inner(*args, **kwargs):
    try:
      payload = args[0]

      if not is_uuid(payload[0]):
        raise ValueError

      return func(*args, **kwargs)
    except ValueError:
      print("Give me valid id(UUID)")

  return inner

def add_car_number_validation(func):
  def inner(*args, **kwargs):
    try:
      payload = args[0]

      if not is_uuid(payload[0]):
        raise ValueError

      if not is_car_number(payload[1]):
        raise ValueError

      return func(*args, **kwargs)
    except ValueError:
      print("Give me valid id(UUID) and car_number(XX 1234 XX) please.")

  return inner
