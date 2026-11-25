from fastapi import FastAPI, HTTPException, status
from mysql.connector import IntegrityError
from database import DatabaseConnection
from models import CursoCreate, CursoUpdate, CursoResponse
from repository import CursoRepository


class CursoServiceApp:
    """Clase principal que configura y expone los endpoints del Microservicio de Cursos."""

    def __init__(self):
        self.app = FastAPI(
            title="Microservicio de Cursos - Universidad XYZ",
            description="API RESTful con POO y Procedimientos Almacenados para gestión de cursos",
            version="1.0.0",
        )
        db = DatabaseConnection()
        self.repo = CursoRepository(db)
        self._register_routes()

    def _register_routes(self):
        @self.app.post(
            "/cursos",
            response_model=CursoResponse,
            status_code=status.HTTP_201_CREATED,
            tags=["Cursos"],
        )
        def crear_curso(curso: CursoCreate):
            try:
                return self.repo.crear(curso)
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El código del curso ya existe.",
                )

        @self.app.get(
            "/cursos",
            response_model=list[CursoResponse],
            tags=["Cursos"],
        )
        def listar_cursos():
            return self.repo.listar_todos()

        @self.app.get(
            "/cursos/{curso_id}",
            response_model=CursoResponse,
            tags=["Cursos"],
        )
        def obtener_curso(curso_id: int):
            curso = self.repo.obtener_por_id(curso_id)
            if not curso:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Curso no encontrado.",
                )
            return curso

        @self.app.put(
            "/cursos/{curso_id}",
            response_model=CursoResponse,
            tags=["Cursos"],
        )
        def actualizar_curso(curso_id: int, curso: CursoUpdate):
            try:
                actualizado = self.repo.actualizar(curso_id, curso)
                if not actualizado:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Curso no encontrado.",
                    )
                return actualizado
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El código ya pertenece a otro curso.",
                )

        @self.app.delete(
            "/cursos/{curso_id}",
            status_code=status.HTTP_200_OK,
            tags=["Cursos"],
        )
        def eliminar_curso(curso_id: int):
            eliminado = self.repo.eliminar(curso_id)
            if not eliminado:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Curso no encontrado.",
                )
            return {"mensaje": "Curso eliminado correctamente."}


service = CursoServiceApp()
app = service.app