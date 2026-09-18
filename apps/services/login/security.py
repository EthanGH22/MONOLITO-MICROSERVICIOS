"""Hash de contraseña con PBKDF2. Nunca se persiste el texto plano."""

from werkzeug.security import check_password_hash, generate_password_hash

METHOD = "pbkdf2:sha256:600000"


def hash_password(plain):
    return generate_password_hash(plain, method=METHOD)


def verify_password(password_hash, plain):
    if not password_hash:
        return False
    return check_password_hash(password_hash, plain)
