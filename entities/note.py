class Note:
  def __init__(self, text) -> None:
    self.text= text 

class Tag:
  def __init__(self, name) -> None:
    self.name = name

class NoteBook:
  def __init__(self) -> None:
    self.notes = []
  
  def add_note(self, note):
    self.notes.append(note)
