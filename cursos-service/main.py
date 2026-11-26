from fastapi import FastAPI, HTTPException, status
from mysql.connector import IntegrityError
from models import CursoCreate, CursoUpdate, CursoResponse
from repository import CursoRepository

class CursoServiceApp:
    def __init__(self):
        self.app = FastAPI(title="Microservicio de Cursos - Universidad XYZ", version="1.0.0")
        self.repo = CursoRepository()
        self._register_routes()

    def _register_routes(self):
        @self.app.post("/cursos", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
        def crear_curso(curso: CursoCreate):
            try:
                nuevo_id = self.repo.crear(curso)
                return CursoResponse(id=nuevo_id, **curso.model_dump())
            except IntegrityError:
                raise HTTPException(status_code=400, detail="El código del curso ya está registrado.")

        @self.app.get("/cursos", response_model=list[CursoResponse])
        def listar_cursos():
            return self.repo.listar()

        @self.app.get("/cursos/{curso_id}", response_model=CursoResponse)
        def obtener_curso(curso_id: int):
            item = self.repo.obtener(curso_id)
            if not item:
                raise HTTPException(status_code=404, detail="Curso no encontrado.")
            return item

        @self.app.put("/cursos/{curso_id}", response_model=CursoResponse)
        def actualizar_curso(curso_id: int, curso: CursoUpdate):
            actualizado = self.repo.actualizar(curso_id, curso)
            if not actualizado:
                raise HTTPException(status_code=404, detail="Curso no encontrado.")
            return self.repo.obtener(curso_id)

        @self.app.delete("/cursos/{curso_id}")
        def eliminar_curso(curso_id: int):
            eliminado = self.repo.eliminar(curso_id)
            if not eliminado:
                raise HTTPException(status_code=404, detail="Curso no encontrado.")
            return {"mensaje": "Curso eliminado correctamente"}

service = CursoServiceApp()
app = service.app
