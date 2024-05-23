import re


class Note:
    def __init__(self, id: str, text: str) -> None:
        self.id = id
        self.text = text

    def get_text(self) -> str:
        return self.text

    def get_id(self) -> str:
        return self.id

    def set_text(self, new_text: str):
        self.text = new_text


class NoteBook:
    def __init__(self) -> None:
        self.tags_map = {}
        self.notes = []

    def add_note_with_tads_parse(self, id, note_txt: str):
        new_note_tags = self.__parse_note_tags(note_txt)
        note = Note(id, note_txt)

        self.notes.append(note)

        self.__add_note_to_tags_map(new_note_tags, note)

        return {
            "result": True,
            "note": note,
            "tags": new_note_tags
        }

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

    def get_all_tags(self):
        return sorted(self.tags_map.keys())

    def update_note_by_id(self, id: str, new_text: str):
        note = self.get_note_by_id(id)

        if not note:
            return False

        self.__remove_old_note_tags(note)

        new_note_tags = self.__parse_note_tags(new_text)
        note.set_text(new_text)

        self.__add_note_to_tags_map(new_note_tags, note)

        return True

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

    def delete_note_by_id(self, id: str):
        note = self.get_note_by_id(id)

        if not note:
            return False

        self.__remove_old_note_tags(note)
        self.notes = list(filter(lambda note: note.get_id() != id, self.notes))

        return True
