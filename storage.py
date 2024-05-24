import pickle
from pathlib import Path
from uuid import uuid4
from entities import AddressBook, Name, Phone, Id, Birthday, Plate, Contact, Email, Address
from note import NoteBook, Note

_NAME_FIELD_KEY = "Name"
_PHONE_FIELD_KEY = "Phone"

@DeprecationWarning
def add_user_to_store(name, phone):
    id_record = Id()
    name_record = Name(name)
    phone_record = Phone(phone)
    new_record = address_book.add_contact(id_record, name_record, phone_record)
    serialize_address_book()

    return new_record

def add_contact(name: Name, phone: Phone) -> Contact:
    contact: Contact = address_book.add_contact(Id(), name, phone)
    serialize_address_book()

    return contact

def find_all_users_from_store():
    return address_book.get_records()

@DeprecationWarning
def update_user_by_id(id, new_name, new_phone):
    result = address_book.update_record_by_id(id, new_name, new_phone)
    serialize_address_book()
    return result

def update_contact(id: Id, new_name: Name, new_phone: Phone) -> Contact:
    result = address_book.update_contact(id, new_name, new_phone)
    serialize_address_book()
    return result

def remove_contact(id: Id) -> Contact:
    result = address_book.remove_contact(id)
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

@DeprecationWarning
def update_birthday_val(id, date):
    result = address_book.update_birthday_val(id, date)
    serialize_address_book()
    return result


def update_birthday(id: Id, birthday: Birthday) -> Contact:
    contact: Contact = address_book.update_birthday(id, birthday)
    serialize_address_book()

    return contact


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
    email = Email(email)
    result = address_book.add_email(id, email)
    serialize_address_book()
    return result

@DeprecationWarning
def edit_email_by_id(id, email):
    result = address_book.update_email_by_id(id, email)
    serialize_address_book()
    return result


def update_email(id: Id, email: Email) -> Contact:
    contact: Contact = address_book.update_email(id, email)
    serialize_address_book()

    return contact


def update_plate(id: Id, plate: Plate) -> Contact:
    contact: Contact = address_book.update_plate(id, plate)
    serialize_address_book()

    return contact

def update_address(id: Id, addpress: Address) -> Contact:
    contact: Contact = address_book.update_address(id, addpress)
    serialize_address_book()

    return contact

def add_car_number_to_user(id, number):
    car_number = Plate(number)
    result = address_book.add_car_number_by_id(id, car_number)
    serialize_address_book()
    return result


def update_car_number(id, number):
    result = address_book.update_car_number(id, number)
    serialize_address_book()
    return result

def get_contact_by_id(id: Id) -> Contact:
    return address_book.get_contact_by_id(id)


def get_contact_by_id_new(id: Id) -> Contact:
    return address_book.get_contact_by_id(id)


@DeprecationWarning
def get_contact_by_name_val(name: str) -> Contact:
    return address_book.get_record_by_field(_NAME_FIELD_KEY, name, None)


def get_contact_by_name(name: Name) -> Contact:
    return address_book.get_contact_by_name(name)


def get_contact_by_phone(phone: Phone) -> Contact:
    return address_book.get_contact_by_phone(phone)


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


def add_new_note(new_note: Note):
    res = note_book.add_note_with_tads_parse(new_note)
    serialize_note_book()
    return res

def get_note_by_id(id: str):
    res = note_book.get_note_by_id(id)
    return res

def edit_note_by_id(id, updated_note: Note):
    res = note_book.edit_note_by_id(id, updated_note)
    serialize_note_book()
    return res


def find_all_notes():
    return note_book.get_all_notes()


def find_all_tags():
    return note_book.find_all_tags()


def get_notes_by_tag(tag: str):
    return note_book.get_notes_by_tag(tag)


def find_note_by_id(id: str):
    return note_book.get_note_by_id(id)


def search_notes_by_substring(substring: str):
    return note_book.search_notes_by_substring(substring)


def remove_note(id: str):
    res = note_book.remove_note(id)
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
