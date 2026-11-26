from database import DatabaseConnection
from models import CursoCreate, CursoUpdate

class CursoRepository:
    def __init__(self):
        self.db = DatabaseConnection()

    def crear(self, data: CursoCreate) -> int:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("sp_crear_curso", [data.codigo, data.nombre, data.creditos, data.docente])
            nuevo_id = 0
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    nuevo_id = row[0]
            conn.commit()
            return nuevo_id
        finally:
            cursor.close()
            conn.close()

    def listar(self) -> list[dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_listar_cursos")
            registros = []
            for result in cursor.stored_results():
                registros = result.fetchall()
            return registros
        finally:
            cursor.close()
            conn.close()

    def obtener(self, curso_id: int) -> dict | None:
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_obtener_curso", [curso_id])
            registro = None
            for result in cursor.stored_results():
                registro = result.fetchone()
            return registro
        finally:
            cursor.close()
            conn.close()

    def actualizar(self, curso_id: int, data: CursoUpdate) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("sp_actualizar_curso", [curso_id, data.codigo, data.nombre, data.creditos, data.docente])
            afectados = 0
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    afectados = row[0]
            conn.commit()
            return afectados > 0
        finally:
            cursor.close()
            conn.close()

    def eliminar(self, curso_id: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("sp_eliminar_curso", [curso_id])
            afectados = 0
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    afectados = row[0]
            conn.commit()
            return afectados > 0
        finally:
            cursor.close()
            conn.close()
