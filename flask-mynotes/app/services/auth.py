from werkzeug.datastructures import ImmutableMultiDict
from core import users
from flask import flash, redirect
from flask_login import login_user, logout_user


def load_user_from_session(user_id: str):
    return users.get_authenticated_user_by_id(user_id)


def process_authorization(form_data: ImmutableMultiDict):
    username = form_data.get('username-input')
    password = form_data.get('password-input')
    db_user = users.get_with_password(username, password)
    if db_user is not None:
        login_user(users.AuthenticatedUser(db_user.id, db_user.name))
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
    db_user = users.create_new(username, password)
    login_user(users.AuthenticatedUser(db_user.id, db_user.name))
    flash("Success registration")
    return redirect("/")


def logout():
    logout_user()
