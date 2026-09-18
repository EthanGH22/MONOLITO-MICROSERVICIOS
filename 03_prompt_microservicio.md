1.- Escribe un microservicio en Flask (no blueprints) con una conexión a la base de datos Postgres para generar los endpoints necesarios para las operaciones CRUD de libros. Usa exclusivamente la librería pysicopg. Depositalo en /apps/services/soap

2.- Usa como referencia el esquema de base de datos disponible en /data/schema.sql y el diseo XML de /apps/services/soap/library.xml

3.- El microservicio debe mostrar todos los libros, un libro, buscar por atributos, modificar, borrar y actualizar libros.

4.- Toma en consideración el problema CORS, ya que este microservicio será accedido mediante clientes fuera del dominio.

5.- Los datos de la base de datos de Postgres son: user: library_user, password: 666 y la base de datos: library. Utiliza estos datos de acceso en un archivo .env, no los expongas en el código.

6.- Utiliza Swagger para la documentación del microservicio.