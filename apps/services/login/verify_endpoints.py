"""Ejercicio de todos los endpoints (XML por defecto y JSON)."""

from __future__ import annotations

import json
import uuid
from http.cookiejar import CookieJar
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import HTTPCookieProcessor, Request, build_opener

BASE = "http://127.0.0.1:5000"
OUT = Path(__file__).resolve().parents[3] / "docs" / "evidencia"
OUT.mkdir(parents=True, exist_ok=True)

EMAIL = f"ana.{uuid.uuid4().hex[:8]}@example.com"
PASSWORD = "secreto123"
jar = CookieJar()
opener = build_opener(HTTPCookieProcessor(jar))


def call(method, path, body=None, content_type=None, data=None):
    headers = {}
    payload = data
    if body is not None:
        payload = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = content_type or "application/json"
    elif content_type:
        headers["Content-Type"] = content_type
    req = Request(BASE + path, data=payload, headers=headers, method=method)
    try:
        with opener.open(req) as resp:
            return resp.status, resp.headers.get("Content-Type"), resp.read()
    except HTTPError as exc:
        return exc.code, exc.headers.get("Content-Type"), exc.read()


def save(name, status, ctype, raw):
    text = raw.decode("utf-8")
    (OUT / name).write_text(f"HTTP {status}\nContent-Type: {ctype}\n\n{text}", encoding="utf-8")
    print(f"{name}: {status} {ctype}")
    return text


xml = '<register><nombre>Ana</nombre><apellido_paterno>Lopez</apellido_paterno>' \
      '<apellido_materno>Ruiz</apellido_materno>' \
      f'<email>{EMAIL}</email><password>{PASSWORD}</password></register>'

save("01_health_xml.txt", *call("GET", "/health"))
save("02_health_json.txt", *call("GET", "/health?format=json"))
save(
    "03_register_xml.txt",
    *call("POST", "/register", data=xml.encode("utf-8"), content_type="application/xml"),
)
save(
    "04_register_json_conflict.txt",
    *call(
        "POST",
        "/register?format=json",
        {
            "nombre": "Ana",
            "apellido_paterno": "Lopez",
            "apellido_materno": "Ruiz",
            "email": EMAIL,
            "password": PASSWORD,
        },
    ),
)
save(
    "05_register_invalid_email.txt",
    *call(
        "POST",
        "/register?format=json",
        {
            "nombre": "Ana",
            "apellido_paterno": "Lopez",
            "apellido_materno": "Ruiz",
            "email": "no-es-correo",
            "password": PASSWORD,
        },
    ),
)
save("06_session_anon_xml.txt", *call("GET", "/session"))
save(
    "07_login_xml.txt",
    *call(
        "POST",
        "/login",
        data=f"<login><email>{EMAIL}</email><password>{PASSWORD}</password></login>".encode(),
        content_type="application/xml",
    ),
)
save("08_session_auth_json.txt", *call("GET", "/session?format=json"))
save("09_logout_xml.txt", *call("POST", "/logout"))
save("10_session_after_logout.txt", *call("GET", "/session?format=json"))
save(
    "11_login_json_bad_password.txt",
    *call("POST", "/login?format=json", {"email": EMAIL, "password": "incorrecta"}),
)

print("email=", EMAIL)
print("evidence=", OUT)
