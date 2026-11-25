from fastapi import FastAPI, HTTPException, status
from mysql.connector import IntegrityError
from database import DatabaseConnection
from models import EstudianteCreate, EstudianteUpdate, EstudianteResponse
from repository import EstudianteRepository


class EstudianteServiceApp:
    """Clase principal que configura y expone los endpoints del Microservicio de Estudiantes."""

    def __init__(self):
        self.app = FastAPI(
            title="Microservicio de Estudiantes - Universidad XYZ",
            description="API RESTful con POO y Procedimientos Almacenados para gestión de estudiantes",
            version="1.0.0",
        )
        db = DatabaseConnection()
        self.repo = EstudianteRepository(db)
        self._register_routes()

    def _register_routes(self):
        @self.app.post(
            "/estudiantes",
            response_model=EstudianteResponse,
            status_code=status.HTTP_201_CREATED,
            tags=["Estudiantes"],
        )
        def crear_estudiante(estudiante: EstudianteCreate):
            try:
                return self.repo.crear(estudiante)
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El código o correo del estudiante ya existe.",
                )

        @self.app.get(
            "/estudiantes",
            response_model=list[EstudianteResponse],
            tags=["Estudiantes"],
        )
        def listar_estudiantes():
            return self.repo.listar_todos()

        @self.app.get(
            "/estudiantes/{estudiante_id}",
            response_model=EstudianteResponse,
            tags=["Estudiantes"],
        )
        def obtener_estudiante(estudiante_id: int):
            estudiante = self.repo.obtener_por_id(estudiante_id)
            if not estudiante:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Estudiante no encontrado.",
                )
            return estudiante

        @self.app.put(
            "/estudiantes/{estudiante_id}",
            response_model=EstudianteResponse,
            tags=["Estudiantes"],
        )
        def actualizar_estudiante(estudiante_id: int, estudiante: EstudianteUpdate):
            try:
                actualizado = self.repo.actualizar(estudiante_id, estudiante)
                if not actualizado:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Estudiante no encontrado.",
                    )
                return actualizado
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El código o correo ya pertenece a otro estudiante.",
                )

        @self.app.delete(
            "/estudiantes/{estudiante_id}",
            status_code=status.HTTP_200_OK,
            tags=["Estudiantes"],
        )
        def eliminar_estudiante(estudiante_id: int):
            eliminado = self.repo.eliminar(estudiante_id)
            if not eliminado:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Estudiante no encontrado.",
                )
            return {"mensaje": "Estudiante eliminado correctamente."}


service = EstudianteServiceApp()
app = service.app