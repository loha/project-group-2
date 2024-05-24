import re

@DeprecationWarning
def is_only_chars(value: str):
    return bool(re.match(r"[A-z]+", value))


def validate_name(val: str) -> None:
    if not re.match(R'^[A-z]+\s*[A-z]*$', val):
        raise ValueError("Name must have only chars and spaces")


def is_phone(val: str) -> bool:
    return bool(re.match(r"\+380[0-9]{9}", val))
    

def validate_phone(val: str) -> None:
    # if not is_phone(val):
    if not val.isdigit():
        raise ValueError("Phone must have format '+380XXXXXXXXX'")
    

def is_uuid(uuid_string):
    # UUID version 4 pattern
    pattern = r"[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}"
    return bool(re.match(pattern, uuid_string))


def validate_id(val: str) -> None:
    if not is_uuid(val):
        raise ValueError("Id must have format 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'")


def is_date(value):
    match = re.search(r"^\d{4}\.\d{2}.\d{2}$", value)
    return bool(match)


def is_car_number(value):
    pattern = r'^[A-Z]{2}\d{4}[A-Z]{2}$'
    return bool(re.match(pattern, value))


def is_tag(value):
    return bool(re.match(r"#(\w+)", value))


def is_email(value: str):
    return bool(re.match(r"\w+@\w+\.\w+", value))


def has_valid_address_chars(value):
    return bool(re.match(r"^[a-zA-Z0-9\-\/\s\']+$", value))
