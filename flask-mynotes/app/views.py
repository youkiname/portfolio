from flask import Blueprint, render_template, redirect, request
from app.services import auth, notes
from flask import session, flash

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('home.html', user=session.get('user'), notes=notes.get_last_notes())


@bp.route('/note/<int:note_id>/', methods=['GET'])
def note_page(note_id: int):
    if not session.get('user'):
        flash('You must be logged in!')
        return redirect('/authorization')
    note = notes.get_note_data(note_id)
    return render_template('note_page.html', user=session.get('user'), note=note)


@bp.route('/new_note/', methods=['POST', 'GET'])
def new_note():
    if not session.get('user'):
        flash('You must be logged in!')
        return redirect('/authorization')
    if request.method == "POST":
        result = notes.process_new_note(request.form)
        if result is not None:
            return result
    return render_template('new_note.html', user=session.get('user'))


@bp.route('/remove_note/<int:note_id>/', methods=['GET'])
def remove_note(note_id: int):
    if not session.get('user'):
        flash('You must be logged in!')
        return redirect('/authorization')
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
def logout():
    auth.logout()
    return redirect('/')
