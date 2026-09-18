# Microservicio de autenticación (`apps/services/login`)

Flask + Psycopg 3 + PostgreSQL. Respuestas en **XML** (predeterminado) o **JSON** (`?format=json`).
La contraseña vive como `usuario.password_hash` en la misma fila de la cuenta: no hay tabla de passwords ni segundo almacenamiento.

## Requisitos

- Docker (PostgreSQL 16) o una instancia `library` con usuario `library_user`
- Python 3.11+ (probado con 3.14)

## Base de datos

Desde la raíz del monorepo:

```bash
docker compose up -d postgres
```

El archivo `data/schema.sql` crea el modelo de librería y la tabla `usuario` (email único, `password_hash`, a lo sumo un administrador).

Credenciales de curso (también en `.env`):

- usuario: `library_user`
- password: `666`
- base: `library`

## Arranque en el puerto 5000

```bash
cd apps/services/login
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env   # o cp .env.example .env
python app.py
```

Documentación Swagger: [http://localhost:5000/docs](http://localhost:5000/docs)

## Endpoints

| Método | Ruta | Función |
|--------|------|---------|
| POST | `/register` | Alta de usuario |
| POST | `/login` | Autenticación + sesión Flask |
| POST | `/logout` | Cierre de sesión |
| GET | `/session` | ¿Hay sesión? |
| GET | `/health` | Servicio + PostgreSQL |

`POST /login` y `POST /login?format=xml` responden XML. `POST /login?format=json` responde JSON.

Cuerpo de registro: `nombre`, `apellido_paterno`, `apellido_materno`, `email`, `password`.
El email se valida y debe ser único. El hash usa PBKDF2-SHA256 (Werkzeug).
