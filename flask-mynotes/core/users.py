from core.models import User
from core.passwords import hash_password
from markupsafe import escape


def create_new(username: str, password: str):
    password_hash = hash_password(password)
    User.create(name=username, password_hash=password_hash)


def is_exist(username: str) -> bool:
    return User.get_or_none(User.name == username) is not None


def check_password(username: str, password: str) -> bool:
    password_hash = hash_password(password)
    return User.get_or_none(User.name == username, User.password_hash == password_hash) is not None


def get(username: str) -> User:
    return User.get_or_none(User.name == username)
