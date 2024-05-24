import curses
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
    "21. Get Notes by Text": "find_notes_by_text",
    "22. List Notes": "list_notes"
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
    return key == 127


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
    win.addstr(0, 0, _header(cmd))

    name: str = _read_val_obj(2, "Name", model.Name)
    phone: str = _read_val_obj(4, "Phone", model.Phone)

    contact: model.Contact = repo.add_contact(name, phone)

    msg = f"Contact successfully created"
    win.addstr(6, 0, _header(msg))

    win.addstr(8, 0, str(contact))

    win.addstr(10, 0, "Press any key to continue")
    win.getch()


def get_contact_by_id(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    id: model.Id = _read_val_obj(2, "Id", model.Id)

    contact: model.Contact = repo.get_contact_by_id(id)

    if not contact:
        msg = f"Contact NOT found"
        win.addstr(4, 0, _header(msg))
    else:
        msg = f"Contact found"
        win.addstr(4, 0, _header(msg))
        win.addstr(6, 0, str(contact))

    win.addstr(8, 0, "Press any key to continue")
    win.getch()


def get_contact_by_name(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    name: model.Name = _read_val_obj(2, "Name", model.Name)

    contact: model.Contact = repo.get_contact_by_name(name)

    if not contact:
        msg = f"Contact NOT found"
        win.addstr(4, 0, _header(msg))
    else:
        msg = f"Contact found"
        win.addstr(4, 0, _header(msg))
        win.addstr(6, 0, str(contact))

    win.addstr(8, 0, "Press any key to continue")
    win.getch()


def get_contact_by_phone(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    phone: model.Phone = _read_val_obj(2, "Phone", model.Phone)

    contact: model.Contact = repo.get_contact_by_phone(phone)

    if not contact:
        msg = f"Contact NOT found"
        win.addstr(4, 0, _header(msg))
    else:
        msg = f"Contact found"
        win.addstr(4, 0, _header(msg))
        win.addstr(6, 0, str(contact))

    win.addstr(8, 0, "Press any key to continue")
    win.getch()


def edit_contact(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    id: model.Id = _read_val_obj(2, "Id", model.Id)

    contact: model.Contact = repo.get_contact_by_id(id)

    if not contact:
        msg = f"Contact NOT found"
        win.addstr(4, 0, _header(msg))
        win.addstr(6, 0, "Press any key to continue")
        win.getch()
        return

    win.addstr(4, 0, str(contact))

    name: model.Name = _read_val_obj(6, "Name", model.Name)
    phone: model.Phone = _read_val_obj(8, "Phone", model.Phone)

    contact = repo.update_contact(id, name, phone)

    msg = f"Contact edited successfully"
    win.addstr(10, 0, _header(msg))
    win.addstr(12, 0, str(contact))
    win.addstr(14, 0, "Press any key to continue")
    win.getch()


def remove_contact(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    id: model.Id = _read_val_obj(2, "Id", model.Id)

    contact: model.Contact = repo.get_contact_by_id(id)

    if not contact:
        msg = f"Contact NOT found"
        win.addstr(3, 0, _header(msg))
        win.addstr(5, 0, "Press any key to continue")
        win.getch()
        return

    contact = repo.remove_contact(id)

    msg = f"Contact removed successfully"
    win.addstr(4, 0, _header(msg))
    win.addstr(6, 0, str(contact))
    win.addstr(8, 0, "Press any key to continue")
    win.getch()


def list_contacts(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    contacts: List[model.Contact] = repo.find_all_users_from_store()

    if not contacts:
        msg = f"Contacts NOT found"
        win.addstr(2, 0, _header(msg))
        win.addstr(4, 0, "Press any key to continue")
        win.getch()
        return

    line: int = 2
    for idx, contact in enumerate(contacts):
        line = idx + 2
        if _exceeds_win_size(line, win):
            line -= 2
            win.move(line, 0)
            win.clrtoeol()
            win.addstr(line, 0, "Press any key to continue")
            win.getch()
        win.addstr(line, 0, str(contact))

    if _exceeds_win_size(line + 6, win):
        line = line - 6
        win.move(line, 0)
        win.clrtoeol()

    msg = f"Contact removed successfully"
    win.addstr(two(line), 0, _header(msg))
    win.addstr(two(line), 0, str(contact))
    win.addstr(two(line), 0, "Press any key to continue")
    win.getch()


def edit_birthday(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    id: model.Id = _read_val_obj(2, "Id", model.Id)
    contact: model.Contact = repo.get_contact_by_id(id)

    if not contact:
        msg = f"Contact NOT found"
        win.addstr(4, 0, _header(msg))
        win.addstr(6, 0, "Press any key to continue")
        win.getch()
        return

    win.addstr(4, 0, str(contact))

    birthday: model.Birthday = _read_val_obj(6, "Birthday", model.Birthday)

    contact = repo.update_birthday(id, birthday)

    msg = f"Birthday updated successfully"
    win.addstr(8, 0, _header(msg))
    win.addstr(10, 0, str(contact))
    win.addstr(12, 0, "Press any key to continue")
    win.getch()


def edit_email(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    id: model.Id = _read_val_obj(2, "Id", model.Id)
    contact: model.Contact = repo.get_contact_by_id(id)

    if not contact:
        msg = f"Contact NOT found"
        win.addstr(4, 0, _header(msg))
        win.addstr(6, 0, "Press any key to continue")
        win.getch()
        return

    win.addstr(4, 0, str(contact))

    email: model.Email = _read_val_obj(6, "Email", model.Email)

    contact = repo.update_email(id, email)

    msg = f"Email updated successfully"
    win.addstr(8, 0, _header(msg))
    win.addstr(10, 0, str(contact))
    win.addstr(12, 0, "Press any key to continue")
    win.getch()


def edit_plate(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    id: model.Id = _read_val_obj(2, "Id", model.Id)
    contact: model.Contact = repo.get_contact_by_id(id)

    if not contact:
        msg = f"Contact NOT found"
        win.addstr(4, 0, _header(msg))
        win.addstr(6, 0, "Press any key to continue")
        win.getch()
        return

    win.addstr(4, 0, str(contact))

    email: model.Plate = _read_val_obj(6, "Plate", model.Plate)

    contact = repo.update_plate(id, email)

    msg = f"Plate updated successfully"
    win.addstr(8, 0, _header(msg))
    win.addstr(10, 0, str(contact))
    win.addstr(12, 0, "Press any key to continue")
    win.getch()


def edit_address(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    id: model.Id = _read_val_obj(2, "Id", model.Id)
    contact: model.Contact = repo.get_contact_by_id(id)

    if not contact:
        msg = f"Contact NOT found"
        win.addstr(4, 0, _header(msg))
        win.addstr(6, 0, "Press any key to continue")
        win.getch()
        return

    win.addstr(4, 0, str(contact))

    address: model.Address = _read_val_obj(6, "Address", model.Address)

    contact = repo.update_address(id, address)

    msg = f"Address updated successfully"
    win.addstr(8, 0, _header(msg))
    win.addstr(10, 0, str(contact))
    win.addstr(12, 0, "Press any key to continue")
    win.getch()


def add_note(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    new_note: str = _read_val_obj(2, "Note", note_model.Note)
    
    note: note_model.Note = repo.add_new_note(new_note)

    msg = f"Note successfully created"
    win.addstr(6, 0, _header(msg))

    win.addstr(8, 0, str(note))

    win.addstr(10, 0, "Press any key to continue")
    win.getch()


def get_note_by_id(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    id: note_model.Note = _read_val_obj(2, "Id", str)

    note: model.Contact = repo.get_note_by_id(id)

    if not note:
        msg = f"Note NOT found"
        win.addstr(4, 0, _header(msg))
    else:
        msg = f"Note found"
        win.addstr(4, 0, _header(msg))
        win.addstr(6, 0, str(note))

    win.addstr(8, 0, "Press any key to continue")
    win.getch()


def edit_note(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    id: model.Id = _read_val_obj(2, "Id", str)

    note: note_model.Note = repo.get_note_by_id(id)

    if not note:
        msg = f"Note NOT found"
        win.addstr(4, 0, _header(msg))
        win.addstr(6, 0, "Press any key to continue")
        win.getch()
        return

    win.addstr(4, 0, str(note))

    updated_note: model.Name = _read_val_obj(6, "Note", note_model.Note)

    res = repo.edit_note_by_id(id, updated_note)

    msg = f"Note edited successfully"
    win.addstr(8, 0, _header(msg))
    win.addstr(10, 0, str(res))
    win.addstr(12, 0, "Press any key to continue")
    win.getch()


def list_notes(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    notes: List[model.Contact] = repo.find_all_notes()

    if not notes:
        msg = f"Notes NOT found"
        win.addstr(2, 0, _header(msg))
        win.addstr(4, 0, "Press any key to continue")
        win.getch()
        return
    
    line: int = 2
    for idx, note in enumerate(notes):
        line = idx + 2
        if _exceeds_win_size(line, win):
            line -= 2
            win.move(line, 0)
            win.clrtoeol()
            win.addstr(line, 0, "Press any key to continue")
            win.getch()
        win.addstr(line, 0, str(note))

    if _exceeds_win_size(line + 6, win):
        line = line - 6
        win.move(line, 0)
        win.clrtoeol()

    
    win.addstr(two(line), 0, "Press any key to continue")
    win.getch()


def remove_note(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    id: str = _read_val_obj(2, "Id", str)

    note: model.Contact = repo.get_note_by_id(id)

    if not note:
        msg = f"Note NOT found"
        win.addstr(3, 0, _header(msg))
        win.addstr(5, 0, "Press any key to continue")
        win.getch()
        return

    note = repo.remove_note(id)

    msg = f"Contact removed successfully"
    win.addstr(4, 0, _header(msg))
    win.addstr(6, 0, str(note))
    win.addstr(8, 0, "Press any key to continue")
    win.getch()

def list_tags(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    tags: List[str] = repo.find_all_tags()

    if not tags:
        msg = f"Tags NOT found"
        win.addstr(2, 0, _header(msg))
        win.addstr(4, 0, "Press any key to continue")
        win.getch()
        return
    
    line: int = 2
    for idx, tag in enumerate(tags):
        line = idx + 2
        if _exceeds_win_size(line, win):
            line -= 2
            win.move(line, 0)
            win.clrtoeol()
            win.addstr(line, 0, "Press any key to continue")
            win.getch()
        win.addstr(line, 0, str(tag))

    if _exceeds_win_size(line + 6, win):
        line = line - 6
        win.move(line, 0)
        win.clrtoeol()

    
    win.addstr(two(line), 0, "Press any key to continue")
    win.getch()

def get_notes_by_tag(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    tag: str = _read_val_obj(2, "Tag", str)

    notes: List[note_model.Note] = repo.get_notes_by_tag(tag)

    if not notes:
        msg = f"Notes NOT found"
        win.addstr(2, 0, _header(msg))
        win.addstr(4, 0, "Press any key to continue")
        win.getch()
        return
    
    line: int = 2
    for idx, note in enumerate(notes):
        line = idx + 2
        if _exceeds_win_size(line, win):
            line -= 2
            win.move(line, 0)
            win.clrtoeol()
            win.addstr(line, 0, "Press any key to continue")
            win.getch()
        win.addstr(line, 0, str(note))

    if _exceeds_win_size(line + 6, win):
        line = line - 6
        win.move(line, 0)
        win.clrtoeol()
    
    win.addstr(two(line), 0, "Press any key to continue")
    win.getch()


def find_notes_by_text(cmd: str) -> None:
    win.addstr(0, 0, _header(cmd))

    substring: str = _read_val_obj(2, "Substring", str)

    notes: List[note_model.Note] = repo.search_notes_by_substring(substring)

    if not notes:
        msg = f"Notes NOT found"
        win.addstr(2, 0, _header(msg))
        win.addstr(4, 0, "Press any key to continue")
        win.getch()
        return
    
    line: int = 2
    for idx, note in enumerate(notes):
        line = idx + 2
        if _exceeds_win_size(line, win):
            line -= 2
            win.move(line, 0)
            win.clrtoeol()
            win.addstr(line, 0, "Press any key to continue")
            win.getch()
        win.addstr(line, 0, str(note))

    if _exceeds_win_size(line + 6, win):
        line = line - 6
        win.move(line, 0)
        win.clrtoeol()

    
    win.addstr(two(line), 0, "Press any key to continue")
    win.getch()


def two(line: int) -> int:
    return line + 2


def one(line: int) -> int:
    return line + 1


def _header(text: str):
    return text.center(40, '-') + "\n"


T = TypeVar('T')


def _read_val_obj(line_num: int, field_name: str, cls: Type[T]) -> T:
    info_msg = f"Enter {field_name}: "

    win.addstr(line_num, 0, info_msg)
    while True:
        win.move(line_num, len(info_msg))
        curses.echo()
        raw: bytes = win.getstr(line_num, len(info_msg))
        input: str = raw.decode().strip()

        try:
            return cls(input)
        except ValueError as exp:
            win.addstr(str(exp))
            win.move(line_num, len(info_msg))
            win.clrtoeol()
            continue


if __name__ == '__main__':
    start()
