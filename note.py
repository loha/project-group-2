import re
import validations as check
from uuid import uuid4

class Note:
    def __init__(self, text: str) -> None:
        self.id = str(uuid4())
        self.text = text

    def get_text(self) -> str:
        return self.text

    def get_id(self) -> str:
        return self.id

    def set_text(self, new_text: str):
        self.text = new_text
    
    def __str__(self) -> str:
        return f"Id: {self.id}. Text: {self.text}"


class NoteBook:
    def __init__(self) -> None:
        self.tags_map = {}
        self.notes = []

    def add_note_with_tads_parse(self, note: Note):
        new_note_tags = self.__parse_note_tags(note.get_text())

        self.notes.append(note)

        self.__add_note_to_tags_map(new_note_tags, note)

        return note

    def __parse_note_tags(self, note_txt: str) -> list[str]:
        return re.findall(r"#(\w+)", note_txt)

    def __add_note_to_tags_map(self, tags: list[str], note: Note):
        for tag in tags:
            if tag not in self.tags_map:
                self.tags_map[tag] = []

            if not self.__check_note_in_tags_map(tag, note):
                self.tags_map[tag].append(note)

    def __check_note_in_tags_map(self, tag: str, note: Note) -> bool:
        if tag in self.tags_map:
            if note in self.tags_map[tag]:
                return True

        return False

    def get_all_notes(self) -> list[Note]:
        return self.notes

    def find_all_tags(self):
        return sorted(self.tags_map.keys())

    def edit_note_by_id(self, id: str, updated_note: Note):
        note = self.get_note_by_id(id)

        if not note:
            return None 

        self.__remove_old_note_tags(note)

        text = updated_note.get_text()
        new_note_tags = self.__parse_note_tags(text)
        note.set_text(text)

        self.__add_note_to_tags_map(new_note_tags, note)

        return note

    def get_note_by_id(self, id):
        for note in self.notes:
            if note.get_id() == id:
                return note
        return None

    def __remove_old_note_tags(self, old_note: Note):
        tags_for_delete = []

        for tag in self.tags_map:
            self.tags_map[tag] = list(
                filter(
                    lambda note: note.get_id() != old_note.get_id(),
                    self.tags_map[tag]))

            if len(self.tags_map[tag]) == 0:
                tags_for_delete.append(tag)

        for tag in tags_for_delete:
            del self.tags_map[tag]

    def get_notes_by_tag(self, tag: str):
        if tag in self.tags_map:
            return self.tags_map[tag]
        else:
            return None

    def search_notes_by_substring(self, substring: str):
        res = []
        for note in self.notes:
            if substring in note.get_text():
                res.append(note)

        return res

    def remove_note(self, id: str):
        note = self.get_note_by_id(id)

        if not note:
            return None

        res = str(note)

        self.__remove_old_note_tags(note)
        self.notes = list(filter(lambda note: note.get_id() != id, self.notes))

        return res
