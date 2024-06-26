from dataclasses import dataclass
import datetime
from uuid import uuid4
from helper import is_in_next_7_days
import validations as check
from typing import List


class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Field):
            return self.value.lower() == other.value.lower()
        return False

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

class Id(Field):
    def __init__(self, val: str = None) -> None:
        if val:
            check.validate_id(val)
            super().__init__(val)
        else:
            super().__init__(str(uuid4()))

class Name(Field):
    def __init__(self, value: str) -> None:
        check.validate_name(value)
        super().__init__(value)


class Phone(Field):
    def __init__(self, val: str) -> None:
        check.validate_phone(val)
        super().__init__(val)


class Email(Field):
    def __init__(self, val: str) -> None:
        check.validate_email(val)
        super().__init__(val)


class Birthday(Field):
    def __init__(self, val: str):
        check.validate_date(val)
        super().__init__(val)


class Address(Field):
    def __init__(self, val: str):
        check.validate_address(val)
        super().__init__(val)


class Plate(Field):
    def __init__(self, val: str):
        check.validate_plate(val)
        super().__init__(val)


@dataclass
class Contact:
    id: Id
    name: Name
    phone: Phone
    birthday: Birthday = None
    address: Address = None
    email: Email = None
    plate: Plate = None

    def get_id(self) -> Id:
        return self.id
    
    def get_birthday(self) -> Birthday:
        return self.birthday
    
    def get_name(self) -> Name:
        return self.name

    def __str__(self) -> str:
        return f"Id: {self.id}. Name: {self.name}. Phone: {self.phone}. Birthday: {self.birthday}. Address: {self.address}. Email: {self.email}. Plate: {self.plate}"


class AddressBook:
    def __init__(self) -> None:
        self.records: List[Contact] = []

    def add_contact(self, id: Id, name: Name, phone: Phone) -> Contact:
        contact: Contact = Contact(id, name, phone)
        self.records.append(contact)

        return contact

    def get_contact_by_id(self, id: Id) -> Contact:
        for contact in self.records:
            if contact.id == id:
                return contact

        return None

    def get_contact_by_name(self, name: Name) -> Contact:
        for contact in self.records:
            if contact.name == name:
                return contact

        return None

    def get_contact_by_phone(self, phone: Phone) -> Contact:
        for contact in self.records:
            if contact.phone == phone:
                return contact

        return None
    
    def get_contact_by_plate(self, plate: Plate) -> Contact:
        for contact in self.records:
            if contact.plate == plate:
                return contact

        return None

    def update_contact(self, id: Id, name: Name, phone: Phone) -> Contact:
        contact: Contact = self.get_contact_by_id(id)

        if not contact:
            return None

        contact.name = name
        contact.phone = phone

        return contact

    def add_birthday_by_id(self, id, field: Birthday):
        record = self.get_contact_by_id(id)

        if not record:
            return False

        record.add_field(field)

        return True

    def update_birthday(self, id: Id, birthday: Birthday):
        contact: Contact = self.get_contact_by_id(id)

        if not contact:
            return None

        contact.birthday = birthday

        return contact

    def update_contact(self, id: Id, name: Name, phone: Phone) -> Contact:
        contact: Contact = self.get_contact_by_id(id)

        if not contact:
            return None

        contact.name = name
        contact.phone = phone

        return contact
    
    def update_plate(self, id: Id, plate: Plate) -> Contact:
        contact: Contact = self.get_contact_by_id(id)

        if not contact:
            return None

        contact.plate = plate

        return contact

    def add_address_by_id(self, id, field: Address):
        record = self.get_contact_by_id(id)

        if not record:
            return False

        record.add_field(field)

        return True

    def edit_address_by_id(self, id, address):
        record = self.get_contact_by_id(id)

        if record:
            for field in record.fields:
                field_name = field.get_field_name()

                if field_name == "Address":
                    field.set_value(address)

            return True
        else:
            return False

    def add_email(self, id, field: Email):
        record = self.get_contact_by_id(id)

        if not record:
            return False

        record.add_field(field)

        return True

    def update_email(self, id: Id, email: Email):
        contact: Contact = self.get_contact_by_id(id)

        if not contact:
            return None

        contact.email = email

        return contact

    def update_plate(self, id: Id, plate: Plate):
        contact: Contact = self.get_contact_by_id(id)

        if not contact:
            return None

        contact.plate = plate

        return contact

    def update_address(self, id: Id, address: Address):
        contact: Contact = self.get_contact_by_id(id)

        if not contact:
            return None

        contact.address = address

        return contact

    def get_records(self):
        return list(map(lambda record: str(record).strip(), self.records))

    def get_upcoming_birthdays(self):
        result_records = []
        today = datetime.date.today()
        year = today.year

        for record in self.records:
            birthday: Birthday = record.get_birthday()

            if not birthday:
                continue

            splited_birthday = birthday.value.split(".")
            next_birthday = datetime.date(
                year, int(
                    splited_birthday[1]), int(
                    splited_birthday[2]))

            if is_in_next_7_days(next_birthday, today):
                result_records.append({
                    "name": record.get_name().value,
                    "congratulation_date": next_birthday.strftime("%Y.%m.%d")
                })

        return result_records

    def add_car_number_by_id(self, id, car_number):
        record = self.get_contact_by_id(id)
        has_car_number = False
        result = False

        if not record:
            return result

        for field in record.fields:
            field_name = field.get_field_name()
            if field_name == "CarNumber":
                has_car_number = True

        if not has_car_number:
            record.add_field(car_number)
            result = True

        return result

    def update_car_number(self, id, number):
        record = self.get_contact_by_id(id)

        if record:
            for field in record.fields:
                field_name = field.get_field_name()

                if field_name == "CarNumber":
                    field.set_value(number)

            return True
        else:
            return False

    def remove_contact(self, id: Id) -> Contact:
        contact = self.get_contact_by_id(id)

        if contact:
            deleted_contact = str(contact)
            self.records = list(filter(lambda contact: contact.get_id() != id, self.records))
            return deleted_contact

        return None
