import pickle
from pathlib import Path
from uuid import uuid4
from entities import AddressBook, Name, Phone, Id, Birthday, CarNumber, Record, Email, Address
from note import NoteBook

_NAME_FIELD_KEY = "Name"
_PHONE_FIELD_KEY = "Phone"

def add_user_to_store(name, phone):
  id_record = Id()
  name_record = Name(name)
  phone_record = Phone(phone) 
  new_record = address_book.add_record(id_record, name_record, phone_record)
  serialize_address_book()

  return new_record

def find_all_users_from_store():
  return address_book.get_records()

def update_user_by_id(id, new_name, new_phone):
  result = address_book.update_record_by_id(id, new_name, new_phone)
  serialize_address_book()
  return result

def get_user_phone_by_name(name):
  phone = address_book.get_record_by_field("Name", name, _PHONE_FIELD_KEY)
  return phone

def add_birthday_to_user(id, date):
  birthday = Birthday(date)
  result = address_book.add_birthday_by_id(id, birthday)
  serialize_address_book()
  return result

def update_birthday(id, date):
  result = address_book.update_birthday(id, date)
  serialize_address_book()
  return result

def get_birthday_by_name(name):
  return address_book.get_record_by_field("Name", name, "Birthday")

def get_birthdays():
  return address_book.get_upcoming_birthdays()

def add_address_by_id(id, address):
  address = Address(**address)
  result = address_book.add_address_by_id(id, address)
  serialize_address_book()
  return result

def edit_address_by_id(id, address):
  result = address_book.edit_address_by_id(id, address)
  serialize_address_book()
  return result

def add_email_to_user(id, email):
  email=Email(email)
  result = address_book.add_email(id, email)
  serialize_address_book()
  return result

def edit_email_by_id(id, email):
  result = address_book.update_email_by_id(id, email)
  serialize_address_book()
  return result

def add_car_number_to_user(id, number):
  car_number = CarNumber(number)
  result = address_book.add_car_number_by_id(id, car_number)
  serialize_address_book()
  return result

def update_car_number(id, number):
  result = address_book.update_car_number(id, number)
  serialize_address_book()
  return result

def get_contact_by_name(name: str) -> Record:
  return address_book.get_record_by_field(_NAME_FIELD_KEY, name, None)

def get_contact_by_phone(phone: str) -> Record:
  return address_book.get_record_by_field(_PHONE_FIELD_KEY, phone, None)

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
      set_address_book(address_book)
  except FileNotFoundError:
    pass
    # print("Save file not found")

address_book = AddressBook()

def set_address_book(ab):
  global address_book
  address_book = ab

deserialize_address_book()

#########################
# Notes commands
#########################

def add_new_note(new_note: str):
  id = str(uuid4())
  res = note_book.add_note_with_tads_parse(id, new_note)
  serialize_note_book()
  return res

def update_note_by_id(id, new_text):
  res = note_book.update_note_by_id(id, new_text)
  serialize_note_book()
  return res

def find_all_notes():
  return note_book.get_all_notes()

def find_all_tags():
  return note_book.get_all_tags()

def get_notes_by_tag(tag: str):
  return note_book.get_notes_by_tag(tag)

def find_note_by_id(id: str):
  return note_book.get_note_by_id(id)

def search_notes_by_substring(substring: str):
  return note_book.search_notes_by_substring(substring)

def delete_note_by_id(id: str):
  res = note_book.delete_note_by_id(id)
  serialize_note_book()
  return res

def serialize_note_book():
  current_dir = str(Path(__file__).with_name("note_book.pickle"))
  with open(current_dir, 'wb') as f:
    pickle.dump(note_book, f)

def deserialize_note_book():
  try:
    current_dir = str(Path(__file__).with_name("note_book.pickle"))
    with open(current_dir, 'rb') as f:
      note_book = pickle.load(f)
      set_note_book(note_book)
  except FileNotFoundError:
    pass
    # print("Save file not found")

note_book = NoteBook()

def set_note_book(nb):
  global note_book
  note_book = nb

deserialize_note_book()