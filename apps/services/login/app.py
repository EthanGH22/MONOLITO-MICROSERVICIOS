from pathlib import Path

from flask import Flask, redirect, send_from_directory, session
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from psycopg.errors import OperationalError

import db
import users
from config import HOST, PORT, SECRET_KEY, SESSION_COOKIE_NAME
from respond import parse_body, public_user, requested_format, send
from validators import validate_login, validate_register

ROOT = Path(__file__).resolve().parent
EVIDENCIA = ROOT.parents[3] / "docs" / "evidencia"

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config.update(
    SESSION_COOKIE_NAME=SESSION_COOKIE_NAME,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,
)

CORS(app, supports_credentials=True)

swagger_ui = get_swaggerui_blueprint(
    "/docs",
    "/openapi.yaml",
    config={"app_name": "Login — librería"},
)
app.register_blueprint(swagger_ui, url_prefix="/docs")


def format_or_error():
    fmt = requested_format()
    if fmt is None:
        return None, send(
            {
                "status": "error",
                "message": "El parámetro format debe ser xml o json",
            },
            400,
            "xml",
        )
    return fmt, None


@app.get("/")
def index():
    return redirect("/docs")


@app.get("/openapi.yaml")
def openapi_spec():
    return send_from_directory(ROOT, "openapi.yaml", mimetype="application/yaml")


@app.get("/evidencia/<path:name>")
def evidencia_file(name):
    return send_from_directory(EVIDENCIA, name)


@app.get("/health")
def health():
    fmt, err = format_or_error()
    if err:
        return err
    try:
        db.ping()
        postgres = "ok"
        status_code = 200
        status = "ok"
    except OperationalError as exc:
        postgres = str(exc)
        status_code = 503
        status = "error"
    return send(
        {
            "status": status,
            "service": "login",
            "postgres": postgres,
        },
        status_code,
        fmt,
    )


@app.post("/register")
def register():
    fmt, err = format_or_error()
    if err:
        return err
    payload, errors = validate_register(parse_body())
    if errors:
        return send({"status": "error", "message": errors}, 400, fmt)

    row, conflict = users.create_user(payload)
    if conflict == "email":
        return send(
            {"status": "error", "message": "El correo ya está registrado"},
            409,
            fmt,
        )
    return send(
        {
            "status": "ok",
            "message": "Usuario registrado",
            "user": public_user(row),
        },
        201,
        fmt,
    )


@app.post("/login")
def login():
    fmt, err = format_or_error()
    if err:
        return err
    payload, errors = validate_login(parse_body())
    if errors:
        return send({"status": "error", "message": errors}, 400, fmt)

    row = users.authenticate(payload["email"], payload["password"])
    if not row:
        return send(
            {"status": "error", "message": "Credenciales inválidas"},
            401,
            fmt,
        )

    session.clear()
    session["user_id"] = row["id_usuario"]
    session["email"] = row["email"]
    session.permanent = False
    return send(
        {
            "status": "ok",
            "message": "Sesión iniciada",
            "user": public_user(row),
        },
        200,
        fmt,
    )


@app.post("/logout")
def logout():
    fmt, err = format_or_error()
    if err:
        return err
    session.clear()
    return send({"status": "ok", "message": "Sesión cerrada"}, 200, fmt)


@app.get("/session")
def current_session():
    fmt, err = format_or_error()
    if err:
        return err
    user_id = session.get("user_id")
    if not user_id:
        return send({"status": "ok", "authenticated": False, "user": None}, 200, fmt)

    row = users.find_by_id(user_id)
    if not row:
        session.clear()
        return send({"status": "ok", "authenticated": False, "user": None}, 200, fmt)

    return send(
        {
            "status": "ok",
            "authenticated": True,
            "user": public_user(row),
        },
        200,
        fmt,
    )


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=False)
