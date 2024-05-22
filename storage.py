import pickle
from pathlib import Path
from entities.address_book import AddressBook, Name, Phone, Id, Birthday, CarNumber

def add_user_to_store(name, phone):
  id_record = Id()
  name_record = Name(name)
  phone_record = Phone(phone) 
  new_record = address_book.add_record(id_record, name_record, phone_record)
  serialize_address_book()

  return new_record

def find_all_users_from_store():
  return address_book.get_records()

def update_user_by_id(id, new_name, new_phone, new_birthday):
  result = address_book.update_record_by_id(id, new_name, new_phone, new_birthday)
  serialize_address_book()
  return result

def get_user_phone_by_name(name):
  phone = address_book.get_record_by_field("Name", name, "Phone")
  return phone

def add_birthday_to_user(id, date):
  birthday = Birthday(date)
  result = address_book.add_birthday_by_id(id, birthday)
  serialize_address_book()
  return result;

def get_birthday_by_name(name):
  return address_book.get_record_by_field("Name", name, "Birthday")

def get_birthdays():
  return address_book.get_upcoming_birthdays()

def add_car_number_to_user(id, number):
  car_number = CarNumber(number)
  result = address_book.add_car_number_by_id(id, car_number)
  serialize_address_book()
  return result

def delete_user_by_id(id):
  message = address_book.delete_record_by_id(id)
  serialize_address_book()
  return message

def serialize_address_book():
  current_dir = str(Path(__file__).with_name("address_book.pickle"))
  with open(current_dir, 'wb') as f:
    pickle.dump(address_book, f)

def deserialize_address_book():
  try:
    current_dir = str(Path(__file__).with_name("address_book.pickle"))
    with open(current_dir, 'rb') as f:
      address_book = pickle.load(f)
      set_address_book(address_book);
  except FileNotFoundError:
    print("Save file not found")

address_book = AddressBook()

def set_address_book(ab):
  global address_book
  address_book = ab

deserialize_address_book()
