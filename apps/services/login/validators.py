import re

from email_validator import EmailNotValidError, validate_email

EMAIL_FALLBACK = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def field(data, *names):
    for name in names:
        if name in data and data[name] is not None:
            return str(data[name]).strip()
    return ""


def validate_register(data):
    errors = []
    nombre = field(data, "nombre")
    apellido_paterno = field(data, "apellido_paterno", "apellidoPaterno")
    apellido_materno = field(data, "apellido_materno", "apellidoMaterno")
    email = field(data, "email", "correo")
    password = field(data, "password", "contrasena", "contraseña")

    if not nombre:
        errors.append("nombre es obligatorio")
    elif len(nombre) > 80:
        errors.append("nombre no debe superar 80 caracteres")

    if not apellido_paterno:
        errors.append("apellido paterno es obligatorio")
    elif len(apellido_paterno) > 80:
        errors.append("apellido paterno no debe superar 80 caracteres")

    if not apellido_materno:
        errors.append("apellido materno es obligatorio")
    elif len(apellido_materno) > 80:
        errors.append("apellido materno no debe superar 80 caracteres")

    if not email:
        errors.append("email es obligatorio")
    else:
        email, email_error = normalize_email(email)
        if email_error:
            errors.append(email_error)

    if not password:
        errors.append("password es obligatorio")
    elif len(password) < 8:
        errors.append("password debe tener al menos 8 caracteres")

    cleaned = {
        "nombre": nombre,
        "apellido_paterno": apellido_paterno,
        "apellido_materno": apellido_materno,
        "email": email,
        "password": password,
    }
    return cleaned, errors


def validate_login(data):
    errors = []
    email = field(data, "email", "correo")
    password = field(data, "password", "contrasena", "contraseña")

    if not email:
        errors.append("email es obligatorio")
    else:
        email, email_error = normalize_email(email)
        if email_error:
            errors.append(email_error)

    if not password:
        errors.append("password es obligatorio")

    return {"email": email, "password": password}, errors


def normalize_email(email):
    try:
        result = validate_email(email, check_deliverability=False)
        return result.normalized, None
    except EmailNotValidError as exc:
        if EMAIL_FALLBACK.match(email):
            return email.lower(), None
        return email, f"email inválido: {exc}"
