-- Copia canónica: ver data/schema.sql
-- Librería en línea (PostgreSQL)
-- Normalización 3FN: catálogos independientes, N:M para autores/géneros/conceptos,
-- imágenes 1:N. La cuenta de usuario guarda password_hash (nunca texto plano,
-- nunca una tabla exclusiva de contraseñas).

CREATE TABLE IF NOT EXISTS formato (
    id_formato  SERIAL PRIMARY KEY,
    nombre      VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS categoria (
    id_categoria SERIAL PRIMARY KEY,
    nombre       VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS genero (
    id_genero SERIAL PRIMARY KEY,
    nombre    VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS autor (
    id_autor SERIAL PRIMARY KEY,
    nombre   VARCHAR(120) NOT NULL,
    apellido VARCHAR(120) NOT NULL,
    UNIQUE (nombre, apellido)
);

-- Cuenta de usuario: credenciales y perfil en la misma fila.
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario        SERIAL PRIMARY KEY,
    nombre            VARCHAR(80)  NOT NULL,
    apellido_paterno  VARCHAR(80)  NOT NULL,
    apellido_materno  VARCHAR(80)  NOT NULL DEFAULT '',
    email             VARCHAR(255) NOT NULL,
    password_hash     TEXT         NOT NULL,
    es_administrador  BOOLEAN      NOT NULL DEFAULT FALSE,
    creado_en         TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    CONSTRAINT usuario_email_formato CHECK (position('@' IN email) > 1),
    CONSTRAINT usuario_email_unico UNIQUE (email)
);

-- Como máximo un administrador en toda la plataforma.
CREATE UNIQUE INDEX IF NOT EXISTS uq_un_solo_administrador
    ON usuario (es_administrador)
    WHERE es_administrador IS TRUE;

CREATE TABLE IF NOT EXISTS libro (
    isbn              VARCHAR(17) PRIMARY KEY,
    titulo            VARCHAR(255) NOT NULL,
    anio_publicacion  SMALLINT     NOT NULL CHECK (anio_publicacion BETWEEN 1000 AND 2100),
    precio            NUMERIC(12, 2) NOT NULL CHECK (precio >= 0),
    stock             INTEGER      NOT NULL DEFAULT 0 CHECK (stock >= 0),
    id_formato        INTEGER      NOT NULL REFERENCES formato (id_formato),
    id_categoria      INTEGER      NOT NULL REFERENCES categoria (id_categoria)
);

CREATE TABLE IF NOT EXISTS libro_autor (
    isbn     VARCHAR(17) NOT NULL REFERENCES libro (isbn) ON DELETE CASCADE,
    id_autor INTEGER     NOT NULL REFERENCES autor (id_autor) ON DELETE RESTRICT,
    PRIMARY KEY (isbn, id_autor)
);

CREATE TABLE IF NOT EXISTS libro_genero (
    isbn      VARCHAR(17) NOT NULL REFERENCES libro (isbn) ON DELETE CASCADE,
    id_genero INTEGER     NOT NULL REFERENCES genero (id_genero) ON DELETE RESTRICT,
    PRIMARY KEY (isbn, id_genero)
);

CREATE TABLE IF NOT EXISTS concepto (
    id_concepto SERIAL PRIMARY KEY,
    termino     VARCHAR(120) NOT NULL UNIQUE
);

-- Un mismo concepto puede definirse distinto en cada libro.
CREATE TABLE IF NOT EXISTS libro_concepto (
    isbn        VARCHAR(17) NOT NULL REFERENCES libro (isbn) ON DELETE CASCADE,
    id_concepto INTEGER     NOT NULL REFERENCES concepto (id_concepto) ON DELETE RESTRICT,
    definicion  TEXT        NOT NULL,
    PRIMARY KEY (isbn, id_concepto)
);

CREATE TABLE IF NOT EXISTS imagen (
    id_imagen SERIAL PRIMARY KEY,
    isbn      VARCHAR(17) NOT NULL REFERENCES libro (isbn) ON DELETE CASCADE,
    url       TEXT        NOT NULL,
    alt_text  VARCHAR(255)
);

INSERT INTO formato (nombre) VALUES ('Tapa blanda'), ('Tapa dura'), ('eBook')
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO categoria (nombre) VALUES ('General'), ('Académico'), ('Infantil')
ON CONFLICT (nombre) DO NOTHING;
