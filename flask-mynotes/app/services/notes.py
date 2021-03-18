from werkzeug.datastructures import ImmutableMultiDict
from core import notes, users
from flask import flash
from markupsafe import escape
from flask_login import current_user


def process_new_note(form_data: ImmutableMultiDict):
    title = form_data.get('title-input')
    text = form_data.get('text-input')
    if not title or not text:
        return
    if current_user.is_authenticated:
        db_user = users.get(username=current_user.name)
        notes.create_new(db_user, escape(title), escape(text))
        flash("Success")


def get_last_notes() -> list:
    if not current_user.is_authenticated:
        return []
    return notes.get_last_notes(current_user.name)


def get_note_data(note_id: int) -> dict or None:
    if not current_user.is_authenticated:
        return
    user_db = users.get(current_user.name)
    note = notes.get(note_id)
    if note is None:
        flash("Note {} does not exist".format(note_id))
        return
    if note.user.name != user_db.name:
        flash("You haven't access to this note")
        return
    return note.to_dict()


def try_remove_note(note_id: int):
    if current_user.is_authenticated and notes.check_note_owner(note_id, current_user.name):
        notes.remove_note(note_id)
