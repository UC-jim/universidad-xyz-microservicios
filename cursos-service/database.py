import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self):
        self.config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "db_cursos",
            "port": 3306
        }

    def get_connection(self):
        try:
            return mysql.connector.connect(**self.config)
        except Error as e:
            raise RuntimeError(f"Error de conexión a MySQL: {e}")
