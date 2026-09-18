Diseña una base de datos para una aplicación web monolítica que gestione una librería en línea mediante acceso directo a PostgreSQL.

El diseño debe de contemplar la administración de usuarios registrados, manejar imágenes y conservar definiciones de conceptos asociadas a cada libro.

El diseño base debe partir que todo libro tiene ISBN, título, autor, año de publicación, género, precio, stock, formato, imágenes y conceptos definidos por libro, identifica dependencias funcionales y multivaluadas.
· Un libro puede tener varios autores.
· Un libro puede pertenecer a varios géneros.
· Un libro puede definir muchos conceptos y un mismo concepto puede aparecer en distintos libros con definiciones diferentes.
· Un libro puede tener varias imágenes.
· Formato y categoría son catálogos independientes.
· Debe existir como máximo un administrador.

El diseño final de la base de datos en PostgreSQL depositalo en un archivo .sql en el directorio db/schema.sql. Crea el directorio si no existe.