import curses
import sys
from typing import List, Dict, Any, Type, TypeVar

import entities as model
import note as note_model
import storage as repo

cmd_to_func: Dict[str, str] = {
    "1. Add Contact": "add_contact",
    "2. Edit Contact": "edit_contact",
    "3. Remove Contact": "remove_contact",
    "4. Get Contact by Id": "get_contact_by_id",
    "5. Get Contact by Name": "get_contact_by_name",
    "6. Get Contact by Phone": "get_contact_by_phone",
    "7. Get Contact by Plate": "get_contact_by_plate",
    "8. List Contacts": "list_contacts",

    "9. Edit Birthday": "edit_birthday",
    "10. Edit Address": "edit_address",
    "11. Edit Email": "edit_email",
    "12. Edit Plate": "edit_plate",

    "13. Get Greetin Days": "get_greeting_days",

    "14. Add Note": "add_note",
    "15. Edit Note": "edit_note",
    "16. Edit Note": "edit_note",
    "17. Remove Note": "remove_note",
    "18. Get Note by Id": "get_note_by_id",
    "19. List Tags": "list_tags",
    "20. Get Notes by Tag": "get_notes_by_tag",
    "21. Get Notes by Text": "get_notes_by_text",
    "22. List Notes": "list_notes",
    "0. Exit": "exit"
}


win: curses.window = None


def start():
    curses.wrapper(curses_start)


def curses_start(window: curses.window) -> str:
    curses.curs_set(1)
    global win
    win = window

    while True:
        command = find_command()
        process_command(command)


def find_command() -> str:
    query: str = ""
    filtered_cmds: List[str] = list(cmd_to_func.keys())

    while True:
        win.clear()

        win.refresh()
        msg = "Start typing the command: " + query
        win.addstr(0, 0, msg)

        for idx, cmd in enumerate(filtered_cmds):
            next_line_pos = idx+2

            if next_line_pos == 2:
                win.addstr(next_line_pos, 0, "=> " + cmd)
                continue

            if _exceeds_win_size(next_line_pos, win):
                continue

            win.addstr(next_line_pos, 0, cmd)

        win.move(0, len(msg))
        win.refresh()

        key: int = win.getch()

        if _is_enter(key) and filtered_cmds:
            return filtered_cmds[0]

        query = _process_key(key, query)

        filtered_cmds = _filter_cmds(query)


def _exceeds_win_size(y_pos: int, win):
    max_y = win.getmaxyx()[0]
    return y_pos >= max_y


def _is_enter(key: int):
    return key == 10


def _process_key(key: int, query: str) -> str:
    if _is_backspace(key):
        return query[:-1]

    if _is_escape(key):
        return ""

    if _is_printable(key):
        query += chr(key)
        return query

    return query


def _is_backspace(key: int):
    return key == 127 or key == 263


def _is_escape(key: int):
    return key == 27


def _is_printable(key: int):
    return 32 <= key <= 126


def _filter_cmds(query: str) -> List[str]:
    cmds = list(cmd_to_func.keys())
    return [cmd for cmd in cmds if query.lower() in cmd.lower()]


def process_command(cmd: str) -> None:
    win.clear()

    func: str = cmd_to_func[cmd]
    globs: Dict[str, Any] = globals()

    globs[func](cmd)


def add_contact(cmd: str) -> None:
    _print_header(cmd)

    name: str = _read_val_obj(2, model.Name)
    phone: str = _read_val_obj(4, model.Phone)

    contact: model.Contact = repo.add_contact(name, phone)

    win.addstr(6, 0, _border(SUCCESS_MSG))
    win.addstr(8, 0, str(contact))

    win.addstr(10, 0, PRESS_KEY_MSG)
    win.getch()


PRESS_KEY_MSG = "Press any key to continue"
SUCCESS_MSG = "Operation successful"


def _print_header(cmd: str):
    win.addstr(0, 0, _border(cmd))


def get_contact_by_id(cmd: str) -> None:
    _print_header(cmd)

    id: model.Id = _read_val_obj(2, model.Id)
    ent: model.Contact = repo.get_contact_by_id(id)

    _print_get_footer(ent)


# Main Entity Type
E = TypeVar('E')


def _print_get_footer(ent: E) -> None:
    if not ent:
        win.addstr(4, 0, _border("entity NOT found"))
        win.addstr(6, 0, PRESS_KEY_MSG)
    else:
        win.addstr(4, 0, _border("entity found"))
        win.addstr(6, 0, str(ent))
        win.addstr(8, 0, PRESS_KEY_MSG)

    win.getch()


def get_contact_by_name(cmd: str) -> None:
    _print_header(cmd)

    name: model.Name = _read_val_obj(2, model.Name)
    ent: model.Contact = repo.get_contact_by_name(name)

    _print_get_footer(ent)


def get_contact_by_phone(cmd: str) -> None:
    _print_header(cmd)

    phone: model.Phone = _read_val_obj(2, model.Phone)
    ent: model.Contact = repo.get_contact_by_phone(phone)

    _print_get_footer(ent)


def get_contact_by_plate(cmd: str) -> None:
    _print_header(cmd)

    phone: model.Plate = _read_val_obj(2, model.Plate)
    ent: model.Contact = repo.get_contact_by_plate(phone)

    _print_get_footer(ent)


def edit_contact(cmd: str) -> None:
    _print_header(cmd)

    id: model.Id = _read_val_obj(2, model.Id)
    src_ent: model.Contact = repo.get_contact_by_id(id)

    _print_edit_content(src_ent)

    name: model.Name = _read_val_obj(6, model.Name)
    phone: model.Phone = _read_val_obj(8, model.Phone)

    tgt_ent: model.Contact = repo.update_contact(id, name, phone)

    win.addstr(10, 0, _border(SUCCESS_MSG))
    win.addstr(12, 0, str(src_ent))
    win.addstr(14, 0, PRESS_KEY_MSG)
    win.getch()


def remove_contact(cmd: str) -> None:
    _print_header(cmd)

    id: model.Id = _read_val_obj(2, model.Id)
    src_ent: model.Contact = repo.get_contact_by_id(id)

    _print_edit_content(src_ent)

    tgt_ent = repo.remove_contact(id)

    _print_edit_footer(tgt_ent)


def list_contacts(cmd: str) -> None:
    _print_header(cmd)

    contacts: List[model.Contact] = repo.find_all_users_from_store()

    if not contacts:
        msg = f"Contacts NOT found"
        win.addstr(2, 0, _border(msg))
        win.addstr(4, 0, PRESS_KEY_MSG)
        win.getch()
        return

    line: int = 2
    for idx, contact in enumerate(contacts):
        line = idx + 2
        if _exceeds_win_size(line, win):
            line -= 2
            win.move(line, 0)
            win.clrtoeol()
            win.addstr(line, 0, PRESS_KEY_MSG)
            win.getch()
        win.addstr(line, 0, str(contact))

    if _exceeds_win_size(line + 6, win):
        line = line - 6
        win.move(line, 0)
        win.clrtoeol()

    win.addstr(line + 2, 0, _border("-"))
    win.addstr(line + 4, 0, PRESS_KEY_MSG)
    win.getch()


def edit_birthday(cmd: str) -> None:
    _print_header(cmd)

    id: model.Id = _read_val_obj(2, model.Id)
    src_ent: model.Contact = repo.get_contact_by_id(id)

    _print_edit_content(src_ent)

    birthday: model.Birthday = _read_val_obj(6, model.Birthday)
    tgt_ent: model.Contact = repo.update_birthday(id, birthday)

    _print_edit_footer(tgt_ent)


def _print_edit_content(ent: E) -> None:
    if not ent:
        win.addstr(4, 0, _border("entity NOT found"))
        win.addstr(6, 0, PRESS_KEY_MSG)
        win.getch()
        return

    win.addstr(4, 0, str(ent))


def _print_edit_footer(ent: E) -> None:
    win.addstr(8, 0, _border(SUCCESS_MSG))
    win.addstr(10, 0, str(ent))
    win.addstr(12, 0, PRESS_KEY_MSG)
    win.getch()


def get_greeting_days(cmd: str) -> None:
    win.addstr(0, 0, _border(cmd))

    contacts: List[model.Contact] = repo.get_birthdays()

    if not contacts:
        msg = f"Contacts NOT found"
        win.addstr(2, 0, _border(msg))
        win.addstr(4, 0, PRESS_KEY_MSG)
        win.getch()
        return

    line: int = 2
    for idx, contact in enumerate(contacts):
        line = idx + 2
        if _exceeds_win_size(line, win):
            line -= 2
            win.move(line, 0)
            win.clrtoeol()
            win.addstr(line, 0, PRESS_KEY_MSG)
            win.getch()
        win.addstr(line, 0, str(contact))

    if _exceeds_win_size(line + 6, win):
        line = line - 6
        win.move(line, 0)
        win.clrtoeol()

    win.addstr(line + 2, 0, PRESS_KEY_MSG)
    win.getch()


def edit_email(cmd: str) -> None:
    _print_header(cmd)

    id: model.Id = _read_val_obj(2, model.Id)
    contact: model.Contact = repo.get_contact_by_id(id)

    _print_edit_content(contact)

    email: model.Email = _read_val_obj(6, model.Email)
    contact = repo.update_email(id, email)

    _print_edit_footer(contact)


def edit_plate(cmd: str) -> None:
    _print_header(cmd)

    id: model.Id = _read_val_obj(2, model.Id)
    src_ent: model.Contact = repo.get_contact_by_id(id)

    _print_edit_content(src_ent)

    email: model.Plate = _read_val_obj(6, model.Plate)
    tgt_ent = repo.update_plate(id, email)

    _print_edit_footer(tgt_ent)


def edit_address(cmd: str) -> None:
    _print_header(cmd)

    id: model.Id = _read_val_obj(2, model.Id)
    src_ent: model.Contact = repo.get_contact_by_id(id)

    _print_edit_content(src_ent)

    address: model.Address = _read_val_obj(6, model.Address)
    tgt_ent = repo.update_address(id, address)

    _print_edit_footer(tgt_ent)


def add_note(cmd: str) -> None:
    _print_header(cmd)

    new_note: str = _read_val_obj(2, note_model.Note)

    note: note_model.Note = repo.add_new_note(new_note)

    win.addstr(6, 0, _border(SUCCESS_MSG))
    win.addstr(8, 0, str(note))
    win.addstr(10, 0, PRESS_KEY_MSG)
    win.getch()


def get_note_by_id(cmd: str) -> None:
    _print_header(cmd)

    id: str = _read_val_obj(2, str)
    ent: note_model.Note = repo.get_note_by_id(id)

    _print_get_footer(ent)


def edit_note(cmd: str) -> None:
    _print_header(cmd)

    id: model.Id = _read_val_obj(2, str, "Id")
    src_ent: note_model.Note = repo.get_note_by_id(id)

    _print_edit_content(src_ent)

    note: model.Name = _read_val_obj(6, note_model.Note)
    tgt_ent: note_model.Note = repo.edit_note_by_id(id, note)

    _print_edit_footer(tgt_ent)


def list_notes(cmd: str) -> None:
    _print_header(cmd)

    notes: List[model.Contact] = repo.find_all_notes()

    if not notes:
        msg = f"Notes NOT found"
        win.addstr(2, 0, _border(msg))
        win.addstr(4, 0, PRESS_KEY_MSG)
        win.getch()
        return

    line: int = 2
    for idx, note in enumerate(notes):
        line = idx + 2
        if _exceeds_win_size(line, win):
            line -= 2
            win.move(line, 0)
            win.clrtoeol()
            win.addstr(line, 0, PRESS_KEY_MSG)
            win.getch()
        win.addstr(line, 0, str(note))

    if _exceeds_win_size(line + 6, win):
        line = line - 6
        win.move(line, 0)
        win.clrtoeol()

    win.addstr(line + 2, 0, PRESS_KEY_MSG)
    win.getch()


def remove_note(cmd: str) -> None:
    _print_header(cmd)

    id: str = _read_val_obj(2, str, "Id")
    src_ent: note_model.Note = repo.get_note_by_id(id)

    _print_edit_content(src_ent)

    tgt_ent: note_model.Note = repo.remove_note(id)

    _print_edit_footer


def list_tags(cmd: str) -> None:
    _print_header(cmd)

    tags: List[str] = repo.find_all_tags()

    if not tags:
        msg = f"Tags NOT found"
        win.addstr(2, 0, _border(msg))
        win.addstr(4, 0, PRESS_KEY_MSG)
        win.getch()
        return

    line: int = 2
    for idx, tag in enumerate(tags):
        line = idx + 2
        if _exceeds_win_size(line, win):
            line -= 2
            win.move(line, 0)
            win.clrtoeol()
            win.addstr(line, 0, PRESS_KEY_MSG)
            win.getch()
        win.addstr(line, 0, str(tag))

    if _exceeds_win_size(line + 6, win):
        line = line - 6
        win.move(line, 0)
        win.clrtoeol()

    win.addstr(line + 2, 0, PRESS_KEY_MSG)
    win.getch()


def get_notes_by_tag(cmd: str) -> None:
    _print_header(cmd)

    tag: str = _read_val_obj(2, str, "Tag")

    notes: List[note_model.Note] = repo.get_notes_by_tag(tag)

    if not notes:
        msg = f"Notes NOT found"
        win.addstr(2, 0, _border(msg))
        win.addstr(4, 0, PRESS_KEY_MSG)
        win.getch()
        return

    line: int = 2
    for idx, note in enumerate(notes):
        line = idx + 2
        if _exceeds_win_size(line, win):
            line -= 2
            win.move(line, 0)
            win.clrtoeol()
            win.addstr(line, 0, PRESS_KEY_MSG)
            win.getch()
        win.addstr(line, 0, str(note))

    if _exceeds_win_size(line + 6, win):
        line = line - 6
        win.move(line, 0)
        win.clrtoeol()

    win.addstr(line + 2, 0, PRESS_KEY_MSG)
    win.getch()


def get_notes_by_text(cmd: str) -> None:
    _print_header(cmd)

    substring: str = _read_val_obj(2, str, "Substring")

    notes: List[note_model.Note] = repo.search_notes_by_substring(substring)

    if not notes:
        msg = f"Notes NOT found"
        win.addstr(2, 0, _border(msg))
        win.addstr(4, 0, PRESS_KEY_MSG)
        win.getch()
        return

    line: int = 2
    for idx, note in enumerate(notes):
        line = idx + 2
        if _exceeds_win_size(line, win):
            line -= 2
            win.move(line, 0)
            win.clrtoeol()
            win.addstr(line, 0, PRESS_KEY_MSG)
            win.getch()
        win.addstr(line, 0, str(note))

    if _exceeds_win_size(line + 6, win):
        line = line - 6
        win.move(line, 0)
        win.clrtoeol()

    win.addstr(line + 2, 0, PRESS_KEY_MSG)
    win.getch()


def exit(cmd: str) -> None:
    sys.exit(0)


# Object Value Type
V = TypeVar('V')


def _border(text: str):
    return text.center(40, '-') + "\n"


def _read_val_obj(line: int, cls: Type[V], name: str = None) -> V:
    field_name: str = name if name else cls.__name__

    info_msg = f"Enter {field_name}: "

    win.addstr(line, 0, info_msg)
    while True:
        win.move(line, len(info_msg))
        curses.echo()
        raw: bytes = win.getstr(line, len(info_msg))
        input: str = raw.decode().strip()

        try:
            return cls(input)
        except ValueError as exp:
            win.addstr(str(exp))
            win.move(line, len(info_msg))
            win.clrtoeol()
            continue


if __name__ == '__main__':
    start()
