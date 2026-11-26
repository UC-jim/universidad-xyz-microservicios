from database import DatabaseConnection
from models import EstudianteCreate, EstudianteUpdate

class EstudianteRepository:
    def __init__(self):
        self.db = DatabaseConnection()

    def crear(self, data: EstudianteCreate) -> int:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("sp_crear_estudiante", [
                data.codigo, data.nombres, data.apellidos, data.correo, data.carrera
            ])
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
            cursor.callproc("sp_listar_estudiantes")
            registros = []
            for result in cursor.stored_results():
                registros = result.fetchall()
            return registros
        finally:
            cursor.close()
            conn.close()

    def obtener(self, estudiante_id: int) -> dict | None:
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc("sp_obtener_estudiante", [estudiante_id])
            registro = None
            for result in cursor.stored_results():
                registro = result.fetchone()
            return registro
        finally:
            cursor.close()
            conn.close()

    def actualizar(self, estudiante_id: int, data: EstudianteUpdate) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("sp_actualizar_estudiante", [
                estudiante_id, data.nombres, data.apellidos, data.correo, data.carrera
            ])
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

    def eliminar(self, estudiante_id: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("sp_eliminar_estudiante", [estudiante_id])
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
