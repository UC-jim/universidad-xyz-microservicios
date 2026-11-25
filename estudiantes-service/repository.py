from database import DatabaseConnection
from models import EstudianteCreate, EstudianteUpdate


class EstudianteRepository:
    """Repositorio POO que encapsula el acceso a datos mediante Procedimientos Almacenados."""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def crear(self, estudiante: EstudianteCreate) -> dict:
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc(
                "sp_crear_estudiante",
                [
                    estudiante.codigo,
                    estudiante.nombres,
                    estudiante.apellidos,
                    estudiante.correo,
                    estudiante.carrera,
                ],
            )
            nuevo_id = None
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    nuevo_id = row["id"]
            conn.commit()
            return {"id": nuevo_id, **estudiante.model_dump()}
        finally:
            cursor.close()
            conn.close()

    def listar_todos(self) -> list[dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_listar_estudiantes")
            estudiantes = []
            for result in cursor.stored_results():
                estudiantes = result.fetchall()
            return estudiantes
        finally:
            cursor.close()
            conn.close()

    def obtener_por_id(self, estudiante_id: int) -> dict | None:
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_obtener_estudiante", [estudiante_id])
            for result in cursor.stored_results():
                return result.fetchone()
            return None
        finally:
            cursor.close()
            conn.close()

    def actualizar(self, estudiante_id: int, estudiante: EstudianteUpdate) -> dict | None:
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc(
                "sp_actualizar_estudiante",
                [
                    estudiante_id,
                    estudiante.codigo,
                    estudiante.nombres,
                    estudiante.apellidos,
                    estudiante.correo,
                    estudiante.carrera,
                ],
            )
            affected = 0
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    affected = row["affected_rows"]
            conn.commit()
            if affected == 0 and not self.obtener_por_id(estudiante_id):
                return None
            return {"id": estudiante_id, **estudiante.model_dump()}
        finally:
            cursor.close()
            conn.close()

    def eliminar(self, estudiante_id: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_eliminar_estudiante", [estudiante_id])
            affected = 0
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    affected = row["affected_rows"]
            conn.commit()
            return affected > 0
        finally:
            cursor.close()
            conn.close()