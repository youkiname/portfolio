from flask import Blueprint, render_template, redirect, request
from app.services import auth, notes
from flask_login import current_user, login_required

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('home.html', user=current_user, notes=notes.get_last_notes())


@bp.route('/note/<int:note_id>/', methods=['GET'])
@login_required
def note_page(note_id: int):
    note = notes.get_note_data(note_id)
    return render_template('note_page.html', user=current_user, note=note)


@bp.route('/new_note/', methods=['POST', 'GET'])
@login_required
def new_note():
    if request.method == "POST":
        result = notes.process_new_note(request.form)
        if result is not None:
            return result
    return render_template('new_note.html', user=current_user)


@bp.route('/remove_note/<int:note_id>/', methods=['GET'])
@login_required
def remove_note(note_id: int):
    notes.try_remove_note(note_id)
    return redirect('/')


@bp.route('/authorization/', methods=['POST', 'GET'])
def authorization():
    if request.method == "POST":
        result = auth.process_authorization(request.form)
        if result is not None:
            return result
    return render_template('authorization.html')


@bp.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        result = auth.process_registration(request.form)
        if result is not None:
            return result
    return render_template('registration.html')


@bp.route('/logout/')
@login_required
def logout():
    auth.logout()
    return redirect('/')
