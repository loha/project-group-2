import datetime
from uuid import uuid4
from helper import is_in_next_7_days
import validations as check


class Field:
    def __init__(self) -> None:
        self.field_name = None
        self.value = None

    def get_field_name(self):
        return self.field_name

    def get_field_value(self):
        return self.value

    def set_field_name(self, name):
        self.field_name = name

    def set_value(self, value):
        self.value = value


class Name(Field):
    def __init__(self, value: str) -> None:
        check.validate_name(value)
        super().__init__()
        self.set_field_name("Name")
        self.set_value(value)


class Phone(Field):
    def __init__(self, value: str) -> None:
        check.validate_phone(value)
        super().__init__()
        self.set_field_name("Phone")
        self.set_value(value)


class Email(Field):
    def __init__(self, value) -> None:
        super().__init__()
        self.set_field_name("Email")
        self.set_value(value)


class Id(Field):
    def __init__(self, value: str = None) -> None:
        super().__init__()
        self.set_field_name("ID")
        if value:
            check.validate_id(value)
            self.set_value(value)
        else:
            self.set_value(str(uuid4()))
        
    def __eq__(self, other):
        if isinstance(other, Id):
            return self.value == other.value
        return False


class Birthday(Field):
    def __init__(self, value):
        super().__init__()
        self.set_field_name("Birthday")
        self.set_value(value)


class CarNumber(Field):
    def __init__(self, value):
        self.set_field_name("CarNumber")
        self.set_value(value)


class Contact:
    def __init__(self) -> None:
        # TODO: replace with plain fields
        self.fields = []

    def add_field(self, field):
        self.fields.append(field)

    def get_id(self) -> Id:
        for field in self.fields:
            if field.get_field_name() == "ID":
                return field
        return None

    def get_field_value_by_name(self, field_name):
        for field in self.fields:
            if field.get_field_name() == field_name:
                return field.get_field_value()
        return None

    def __str__(self) -> str:
        res = ""

        for field in self.fields:
            res += f"{field.get_field_name()}: {field.get_field_value()}. "

        return res


# Створено новий клас по додаванню Адресів, переміщений вище AddressBook .
class Address(Field):
    def __init__(
            self,
            country=None,
            city=None,
            street=None,
            house_number=None,
            apartment_number=None):
        super().__init__()
        self.set_field_name("Address")
        self.set_value({
            "Country": country,
            "City": city,
            "Street": street,
            "House Number": house_number,
            "Apartment Number": apartment_number
        })


class AddressBook:
    def __init__(self) -> None:
        self.records = []

    def add_contact(self, *fields) -> Contact:
        contact = Contact()

        for field in fields:
            contact.add_field(field)

        self.records.append(contact)

        return contact
    
    def get_contact_by_id(self, id: Id) -> Contact:
        for contact in self.records:
            if contact.get_id() == id:
                return contact

        return None

    @DeprecationWarning
    def update_record_by_id(self, id, new_name, new_phone):
        record = self.get_contact_by_id(id)

        if record:
            for field in record.fields:
                field_name = field.get_field_name()

                if field_name == "Name":
                    field.set_value(new_name)

                if field_name == "Phone":
                    field.set_value(new_phone)

            return True
        else:
            return False
        

    def update_contact(self, id: Id, new_name: Name, new_phone: Phone) -> Contact:
        contact: Contact = self.get_contact_by_id(id)

        if not contact:
            return None

        for field in contact.fields:
            field_name = field.get_field_name()
            if field_name == "Name":
                field.set_value(new_name.get_field_value())
            if field_name == "Phone":
                field.set_value(new_phone.get_field_value())

        return contact


    @DeprecationWarning
    def get_record_by_id(self, id):
        for record in self.records:
            for field in record.fields:
                if field.get_field_name() == "ID" and field.get_field_value() == id:
                    return record
        return None

    def get_record_by_field(self, search_field, search_value, returned_field):
        for record in self.records:
            for field in record.fields:
                if field.get_field_name() == search_field and field.get_field_value() == search_value:
                    if returned_field:
                        return record.get_field_value_by_name(returned_field)
                    else:
                        return record

        return None

    def add_birthday_by_id(self, id, field: Birthday):
        record = self.get_contact_by_id(id)

        if not record:
            return False

        record.add_field(field)

        return True

    def update_birthday(self, id, date):
        record = self.get_contact_by_id(id)

        if record:
            for field in record.fields:
                field_name = field.get_field_name()

                if field_name == "Birthday":
                    field.set_value(date)

            return True
        else:
            return False

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

    def update_email_by_id(self, id, email):
        record = self.get_contact_by_id(id)

        if record:
            for field in record.fields:
                field_name = field.get_field_name()

                if field_name == "Email":
                    field.set_value(email)

            return True
        else:
            return False

    def get_records(self):
        return list(map(lambda record: str(record).strip(), self.records))

    def get_upcoming_birthdays(self):
        result_records = []
        today = datetime.date.today()
        year = today.year

        for record in self.records:
            splited_birthday = record.get_field_value_by_name(
                'Birthday').split(".")
            next_birthday = datetime.date(
                year, int(
                    splited_birthday[1]), int(
                    splited_birthday[2]))

            if is_in_next_7_days(next_birthday, today):
                result_records.append({
                    "name": record.get_field_value_by_name("Name"),
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

    @DeprecationWarning
    def delete_record_by_id(self, id):
        message = 'Record not found'
        for index, record in enumerate(self.records):
            for field in record.fields:
                if field.get_field_name() == "ID" and field.get_field_value() == id:
                    del self.records[index]
                    message = 'Record deleted'
        return message
    

    def remove_contact(self, id: Id) -> Contact:
        orig_contact: Contact
        for contact in self.records:
            if contact.get_id() == id:
                orig_contact = contact
                del contact
                return orig_contact

        return None
