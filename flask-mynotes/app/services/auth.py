from werkzeug.datastructures import ImmutableMultiDict
from core import users
from flask import session, flash, redirect


def process_authorization(form_data: ImmutableMultiDict):
    username = form_data.get('username-input')
    password = form_data.get('password-input')
    if users.check_password(username, password):
        session['user'] = {"name": username, "logged_in": True}
        flash("Success login")
        return redirect('/')
    else:
        flash("Wrong username or password!")


def process_registration(form_data: ImmutableMultiDict):
    username = form_data.get('username-input')
    password = form_data.get('password-input')
    if users.is_exist(username):
        flash("Username {} already exists".format(username))
        return
    users.create_new(username, password)
    session['user'] = {"name": username, "logged_in": True}
    flash("Success registration")
    return redirect("/")


def logout():
    session['user'] = None
