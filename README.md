# Librería en línea — monorepo

Plataforma de librería con PostgreSQL compartido. Este entregable añade el **microservicio independiente de autenticación** en `apps/services/login` (puerto **5000**, XML/JSON, Swagger, sesiones Flask).

## Estructura

```
data/schema.sql              # Modelo normalizado + usuario.password_hash
docker-compose.yml           # PostgreSQL library / library_user
apps/services/login/         # Microservicio Flask (este ejercicio)
docs/evidencia/              # Capturas de los endpoints
docs/reflexion.md            # Por qué el diseño es así
```

## Cómo levantar autenticación

1. `docker compose up -d postgres`
2. `cd apps/services/login && pip install -r requirements.txt && python app.py`
3. Abrir http://localhost:5000/docs

Detalle operativo: `apps/services/login/README.md`.
