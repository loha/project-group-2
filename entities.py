import datetime
from uuid import uuid4
from helper import is_in_next_7_days

class Field:
  def __init__(self) -> None:
    self.field_name= None
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
  def __init__(self, value) -> None:
    super().__init__()
    self.set_field_name("Name")
    self.set_value(value)

class Phone(Field):
  def __init__(self, value) -> None:
    super().__init__()
    self.set_field_name("Phone")
    self.set_value(value)

class Email(Field):
  def __init__(self, value) -> None:
    super().__init__()
    self.set_field_name("Email")
    self.set_value(value)


class Id(Field):
  def __init__(self) -> None:
    super().__init__()
    self.set_field_name("ID")
    self.set_value(str(uuid4()))

class Birthday(Field):
  def __init__(self, value):
    super().__init__()
    self.set_field_name("Birthday")
    self.set_value(value)

class CarNumber(Field):
  def __init__(self, value):
    self.set_field_name("CarNumber")
    self.set_value(value)

class Record:
  def __init__(self) -> None:
    self.fields = []

  def add_field(self, field):
    self.fields.append(field)

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

class AddressBook:
  def __init__(self) -> None:
    self.records = []

  def add_record(self, *fields):
    record = Record()

    for field in fields:
      record.add_field(field)
    
    self.records.append(record)

    return record
  
  def update_record_by_id(self, id, new_name, new_phone, new_birthday):
    record = self.get_record_by_id(id)

    if record:
      for field in record.fields:
        field_name = field.get_field_name()

        if field_name == "Name":
          field.set_value(new_name)

        if field_name == "Phone":
          field.set_value(new_phone)

        if field_name == "Birthday" and new_birthday is not None:
          field.set_value(new_birthday)

      return True
    else:
      return False
  
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
    record = self.get_record_by_id(id)

    if not record:
      return False
    
    record.add_field(field)

    return True
  
  def add_email(self, id, field: Email):
    record = self.get_record_by_id(id)

    if not record:
      return False
    
    record.add_field(field)

    return True




  def get_records(self):
    return list(map(lambda record: str(record).strip(), self.records))
  
  def get_upcoming_birthdays(self):
    result_records = []
    today = datetime.date.today()
    year = today.year

    for record in self.records:
      splited_birthday = record.get_field_value_by_name('Birthday').split(".")
      next_birthday = datetime.date(year, int(splited_birthday[1]), int(splited_birthday[2]))

      if is_in_next_7_days(next_birthday, today):
        result_records.append({
          "name": record.get_field_value_by_name("Name"),
          "congratulation_date": next_birthday.strftime("%Y.%m.%d")
        })

    return result_records

  def add_car_number_by_id(self, id, car_number):
    record = self.get_record_by_id(id)
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

  def delete_record_by_id(self, id):
    message = 'Record not found'
    for index, record in enumerate(self.records):
        for field in record.fields:
          if field.get_field_name() == "ID" and field.get_field_value() == id:
            del self.records[index]
            message = 'Record deleted'
    return message
