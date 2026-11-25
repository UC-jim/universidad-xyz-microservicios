from database import DatabaseConnection
from models import CursoCreate, CursoUpdate


class CursoRepository:
    """Repositorio POO que encapsula el acceso a datos mediante Procedimientos Almacenados."""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def crear(self, curso: CursoCreate) -> dict:
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc(
                "sp_crear_curso",
                [curso.codigo, curso.nombre, curso.creditos, curso.docente],
            )
            nuevo_id = None
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    nuevo_id = row["id"]
            conn.commit()
            return {"id": nuevo_id, **curso.model_dump()}
        finally:
            cursor.close()
            conn.close()

    def listar_todos(self) -> list[dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_listar_cursos")
            cursos = []
            for result in cursor.stored_results():
                cursos = result.fetchall()
            return cursos
        finally:
            cursor.close()
            conn.close()

    def obtener_por_id(self, curso_id: int) -> dict | None:
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_obtener_curso", [curso_id])
            for result in cursor.stored_results():
                return result.fetchone()
            return None
        finally:
            cursor.close()
            conn.close()

    def actualizar(self, curso_id: int, curso: CursoUpdate) -> dict | None:
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc(
                "sp_actualizar_curso",
                [curso_id, curso.codigo, curso.nombre, curso.creditos, curso.docente],
            )
            affected = 0
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    affected = row["affected_rows"]
            conn.commit()
            if affected == 0 and not self.obtener_por_id(curso_id):
                return None
            return {"id": curso_id, **curso.model_dump()}
        finally:
            cursor.close()
            conn.close()

    def eliminar(self, curso_id: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_eliminar_curso", [curso_id])
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