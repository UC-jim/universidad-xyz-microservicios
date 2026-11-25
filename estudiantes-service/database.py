import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    """Clase encargada de gestionar la conexión a la base de datos de Estudiantes."""

    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.user = "root"
        self.password = ""  # Por defecto en XAMPP la contraseña está vacía
        self.database = "db_estudiantes"

    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            return connection
        except Error as e:
            raise RuntimeError(f"Error al conectar con MySQL: {e}")