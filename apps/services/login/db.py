"""Conexión PostgreSQL con Psycopg 3. Las credenciales salen de DATABASE_URL."""

from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

from config import DATABASE_URL


@contextmanager
def get_conn():
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def ping():
    with get_conn() as conn:
        conn.execute("SELECT 1")
    return True
