from hashlib import sha256


def hash_password(password: str) -> str:
    for i in range(6):
        with_salt = password + "VYNpv2_W"
        password = sha256(with_salt.encode('utf-8')).hexdigest()
    return password
