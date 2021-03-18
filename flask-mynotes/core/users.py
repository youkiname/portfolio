from core.models import User
from core.passwords import hash_password


class AuthenticatedUser:
    is_authenticated = True
    is_active = True
    is_anonymous = False

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def get_id(self):
        return str(self.id)


def get_authenticated_user_by_id(id: str) -> AuthenticatedUser or None:
    try:
        db_user = User.get_by_id(int(id))
        return AuthenticatedUser(db_user.id, db_user.name)
    except Exception:
        return None


def create_new(username: str, password: str) -> User:
    password_hash = hash_password(password)
    return User.create(name=username, password_hash=password_hash)


def is_exist(username: str) -> bool:
    return User.get_or_none(User.name == username) is not None


def get(username: str) -> User:
    return User.get_or_none(User.name == username)


def get_with_password(username: str, password: str) -> User:
    password_hash = hash_password(password)
    return User.get_or_none(User.name == username, User.password_hash == password_hash)


def check_password(username: str, password: str) -> bool:
    return get_with_password(username, password) is not None
