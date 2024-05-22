import pickle
from pathlib import Path
from entities import AddressBook, Name, Phone, Id, Birthday, CarNumber, Record, Email

_NAME_FIELD_KEY = "Name"
_PHONE_FIELD_KEY = "Phone"

def add_user_to_store(name, phone):
  id_record = Id()
  name_record = Name(name)
  phone_record = Phone(phone) 
  new_record = address_book.add_record(id_record, name_record, phone_record)
  serialize()

  return new_record

def find_all_users_from_store():
  return address_book.get_records()

def update_user_by_id(id, new_name, new_phone, new_birthday):
  result = address_book.update_record_by_id(id, new_name, new_phone, new_birthday)
  serialize()
  return result

def get_user_phone_by_name(name):
  phone = address_book.get_record_by_field("Name", name, _PHONE_FIELD_KEY)
  return phone

def add_birthday_to_user(id, date):
  birthday = Birthday(date)
  result = address_book.add_birthday_by_id(id, birthday)
  serialize()
  return result;

def add_email_to_user(id, email):
  email=Email(email)
  result = address_book.add_email(id, email)
  serialize()
  return result;




def get_birthday_by_name(name):
  return address_book.get_record_by_field(_NAME_FIELD_KEY, name, "Birthday")


def get_contact_by_name(name: str) -> Record:
  return address_book.get_record_by_field(_NAME_FIELD_KEY, name, None)


def get_contact_by_phone(phone: str) -> Record:
  return address_book.get_record_by_field(_PHONE_FIELD_KEY, phone, None)

def get_birthdays():
  return address_book.get_upcoming_birthdays()

def add_car_number_to_user(id, number):
  car_number = CarNumber(number)
  result = address_book.add_car_number_by_id(id, car_number)
  serialize()
  return result

def delete_user_by_id(id):
  message = address_book.delete_record_by_id(id)
  serialize()
  return message

def serialize():
  current_dir = str(Path(__file__).with_name("data.pickle"))
  with open(current_dir, 'wb') as f:
    pickle.dump(address_book, f)

def deserialize():
  current_dir = str(Path(__file__).with_name("data.pickle"))
  with open(current_dir, 'rb') as f:
    address_book = pickle.load(f)
    set_address_book(address_book);

address_book = AddressBook()

def set_address_book(ab):
  global address_book
  address_book = ab

# address_book.add_record(Id(), Name("John"), Phone("+380501234567"));
deserialize()
