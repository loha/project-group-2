from validations import is_only_chars, is_phone, is_uuid, is_date, is_car_number, is_tag, is_email, has_valid_address_chars


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
            print(
                "Give me valid user id(should be UUID) or name(only chars) or" +
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


# A-1 Доданий декоратор
def add_address_validation(func):
    def inner(*args, **kwargs):
        try:
            payload = args[0]
            id = payload[0]
            address = {
                "country": payload[1] if len(payload) > 1 else None,
                "city": payload[2] if len(payload) > 2 else None,
                "street": payload[3] if len(payload) > 3 else None,
                "house_number": payload[4] if len(payload) > 4 else None,
                "apartment_number": payload[5] if len(payload) > 5 else None
            }

            if not is_uuid(id):
                raise ValueError('Give me valid UUID')

            for key, value in address.items():
                if key == "apartment_number" and value is None:
                    continue

                if value is None:
                    raise ValueError(f"{key} is required")

                if not has_valid_address_chars(value):
                    raise ValueError(f"{key} has invalid characters")

            return func(*args, **kwargs)
        except ValueError as e:
            print(e)

    return inner


def uuid_validation(func):
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
            print("Give me valid id(UUID) and car_number(XX1234XX) please.")

    return inner


def add_email_validation(func):
    def inner(*args, **kwargs):
        try:
            payload = args[0]

            if not is_uuid(payload[0]):
                raise ValueError

            if not is_email(payload[1]):
                raise ValueError

            return func(*args, **kwargs)
        except ValueError:
            print("Give me correct email(xxx@xx.xx) please.")

    return inner


def add_note_validation(func):
    def inner(*args, **kwargs):
        try:
            payload = args[0]

            first_str = payload[0]
            last_str = payload[len(payload) - 1]
            is_exists_first_double_quote = first_str.split('"')[0] == ""
            splited_last_str = last_str.split('"')
            is_exists_second_double_quote = splited_last_str[len(
                splited_last_str) - 1] == ''

            if is_exists_first_double_quote and is_exists_second_double_quote:
                return func(*args, **kwargs)

            raise ValueError
        except ValueError:
            print("Whats wrong with your note! Please, use double quotes for note text.")

    return inner


def update_note_validation(func):
    def inner(*args, **kwargs):
        try:
            payload = args[0]

            id = payload[0]

            if not is_uuid(id):
                raise ValueError

            new_text = payload[1:]
            first_str = new_text[0]
            last_str = new_text[len(new_text) - 1]
            is_exists_first_double_quote = first_str.split('"')[0] == ""
            splited_last_str = last_str.split('"')
            is_exists_second_double_quote = splited_last_str[len(
                splited_last_str) - 1] == ''

            if is_exists_first_double_quote and is_exists_second_double_quote:
                return func(*args, **kwargs)

            raise ValueError
        except ValueError:
            print("Whats wrong with your note! Please, use double quotes for note text.")

    return inner


def show_notes_by_tag_validation(func):
    def inner(*args, **kwargs):
        try:
            payload = args[0]

            if not is_tag(payload[0]):
                raise ValueError

            return func(*args, **kwargs)
        except ValueError:
            print("Value is not a tag. Please, use #tag_name.")

    return inner


def search_notes_validation(func):
    def inner(*args, **kwargs):
        try:
            payload = args[0]

            # if not is_only_chars(payload[0]):
            #   raise ValueError

            return func(*args, **kwargs)
        except ValueError:
            print("Value is not a tag. Please, use #tag_name.")

    return inner
