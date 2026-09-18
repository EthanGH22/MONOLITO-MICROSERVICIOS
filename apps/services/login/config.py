import os

from dotenv import load_dotenv

load_dotenv()


def env(name, default=None):
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Falta la variable de entorno {name}")
    return value


SECRET_KEY = env("FLASK_SECRET_KEY")
DATABASE_URL = env("DATABASE_URL")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))
SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "library_session")
