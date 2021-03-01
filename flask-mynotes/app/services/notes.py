from werkzeug.datastructures import ImmutableMultiDict
from core import notes, users
from flask import session, flash
from markupsafe import escape


def process_new_note(form_data: ImmutableMultiDict):
    user = session.get('user')
    title = form_data.get('title-input')
    text = form_data.get('text-input')
    if not title or not text:
        return
    db_user = users.get(username=user['name'])
    notes.create_new(db_user, escape(title), escape(text))
    flash("Success")


def get_last_notes() -> list or None:
    user = session.get('user')
    if not user:
        return
    return notes.get_last_notes(user['name'])


def get_note_data(note_id: int) -> dict or None:
    user = session.get('user')
    if not user:
        return
    user_db = users.get(user['name'])
    if not user_db:
        return
    note = notes.get(note_id)
    if note is None:
        flash("Note {} does not exist".format(note_id))
        return
    if note.user.name != user_db.name:
        flash("You haven't access to this note")
        return
    return note.to_dict()


def try_remove_note(note_id: int):
    user = session.get('user')
    if not user:
        return
    if notes.check_note_owner(note_id, user['name']):
        notes.remove_note(note_id)
