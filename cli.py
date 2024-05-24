import curses
import re
from typing import List, Dict, Any, Type, TypeVar

import entities as model
import storage as repo

# Simulated address book
address_book: Dict[int, Dict[str, str]] = {}
next_id: int = 1

cmd_to_func: Dict[str, str] = {
    "Add Contact": "add_contact",
    "Edit Contact": "edit_contact",
    "Remove Contact": "remove_contact",
    "Get Contact by Id": "get_contact_by_id",
    "Get Contact by Name": "get_contact_by_name",
    "Get Contact by Phone": "get_contact_by_phone",
    "List Contacts": "list_contacts",

    "Edit Birthday": "edit_birthday",
    "Edit Address": "edit_address",
    "Edit Plate": "edit_plate",
    "Edit Email": "edit_email",

    "Get Greetin Days": "get_greeting_days",

    "Add Note": "add_note",
    "Update Note": "updaet_note",
    "Remove Note": "remove_note",
    "Get Note by Id": "get_note_by_id",
    "Get Notes by Tag": "get_notes_by_tag",
    "Get Notes by Text": "find_notes_by_text",
    "List Notes": "list_notes"
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
    return [cmd for cmd in cmds if cmd.lower().startswith(query.lower())]


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
        msg = f"Contact NOT found"
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
