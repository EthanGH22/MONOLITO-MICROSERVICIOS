from psycopg.errors import UniqueViolation

from db import get_conn
from security import hash_password, verify_password


def create_user(payload):
    password_hash = hash_password(payload["password"])
    sql = """
        INSERT INTO usuario (
            nombre, apellido_paterno, apellido_materno, email, password_hash
        )
        VALUES (%(nombre)s, %(apellido_paterno)s, %(apellido_materno)s, %(email)s, %(password_hash)s)
        RETURNING id_usuario, nombre, apellido_paterno, apellido_materno, email, es_administrador
    """
    values = {**payload, "password_hash": password_hash}
    values.pop("password", None)
    try:
        with get_conn() as conn:
            row = conn.execute(sql, values).fetchone()
            return row, None
    except UniqueViolation:
        return None, "email"


def find_by_email(email):
    sql = """
        SELECT id_usuario, nombre, apellido_paterno, apellido_materno,
               email, password_hash, es_administrador
        FROM usuario
        WHERE lower(email) = lower(%s)
    """
    with get_conn() as conn:
        return conn.execute(sql, (email,)).fetchone()


def find_by_id(user_id):
    sql = """
        SELECT id_usuario, nombre, apellido_paterno, apellido_materno,
               email, es_administrador
        FROM usuario
        WHERE id_usuario = %s
    """
    with get_conn() as conn:
        return conn.execute(sql, (user_id,)).fetchone()


def authenticate(email, password):
    row = find_by_email(email)
    if not row:
        return None
    if not verify_password(row["password_hash"], password):
        return None
    row.pop("password_hash", None)
    return row
