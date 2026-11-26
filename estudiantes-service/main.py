from fastapi import FastAPI, HTTPException, status
from mysql.connector import IntegrityError
from models import EstudianteCreate, EstudianteUpdate, EstudianteResponse
from repository import EstudianteRepository

class EstudianteServiceApp:
    def __init__(self):
        self.app = FastAPI(title="Microservicio de Estudiantes - Universidad XYZ", version="1.0.0")
        self.repo = EstudianteRepository()
        self._register_routes()

    def _register_routes(self):
        @self.app.post("/estudiantes", response_model=EstudianteResponse, status_code=status.HTTP_201_CREATED)
        def crear_estudiante(estudiante: EstudianteCreate):
            try:
                nuevo_id = self.repo.crear(estudiante)
                return EstudianteResponse(id=nuevo_id, **estudiante.model_dump())
            except IntegrityError:
                raise HTTPException(status_code=400, detail="El código o correo ya está registrado.")

        @self.app.get("/estudiantes", response_model=list[EstudianteResponse])
        def listar_estudiantes():
            return self.repo.listar()

        @self.app.get("/estudiantes/{estudiante_id}", response_model=EstudianteResponse)
        def obtener_estudiante(estudiante_id: int):
            item = self.repo.obtener(estudiante_id)
            if not item:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
            return item

        @self.app.put("/estudiantes/{estudiante_id}", response_model=EstudianteResponse)
        def actualizar_estudiante(estudiante_id: int, estudiante: EstudianteUpdate):
            actualizado = self.repo.actualizar(estudiante_id, estudiante)
            if not actualizado:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
            return self.repo.obtener(estudiante_id)

        @self.app.delete("/estudiantes/{estudiante_id}")
        def eliminar_estudiante(estudiante_id: int):
            eliminado = self.repo.eliminar(estudiante_id)
            if not eliminado:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
            return {"mensaje": "Estudiante eliminado correctamente"}

service = EstudianteServiceApp()
app = service.app
