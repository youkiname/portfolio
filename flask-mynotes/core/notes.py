from core.models import Note, User, DoesNotExist


def create_new(user: User, title: str, text: str):
    Note.create(user=user, title=title, text=text)


def get_last_notes(username: str, limit=20) -> list:
    result = []
    user = User.get_or_none(User.name == username)
    if not user:
        return []
    notes = Note.select().where(Note.user == user).limit(limit).dicts()
    for note in notes:
        result.append(note)
    return result


def check_note_owner(note_id: int, username: str) -> bool:
    user = User.get_or_none(User.name == username)
    if not user:
        return False
    return Note.get_or_none(Note.id == note_id, Note.user == user) is not None


def remove_note(note_id: int):
    try:
        Note.delete_by_id(note_id)
    except DoesNotExist:
        pass


def get(note_id: int) -> Note or None:
    try:
        return Note.get_by_id(note_id)
    except DoesNotExist:
        return None
