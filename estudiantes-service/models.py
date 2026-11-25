from pydantic import BaseModel, EmailStr, Field


class EstudianteBase(BaseModel):
    codigo: str = Field(..., min_length=3, max_length=20, example="EST001")
    nombres: str = Field(..., min_length=2, max_length=100, example="Ana Lucía")
    apellidos: str = Field(..., min_length=2, max_length=100, example="Pérez Gómez")
    correo: EmailStr = Field(..., example="ana.perez@universidad.edu.pe")
    carrera: str = Field(..., min_length=3, max_length=100, example="Ingeniería de Sistemas")


class EstudianteCreate(EstudianteBase):
    """Modelo POO para creación de un estudiante."""
    pass


class EstudianteUpdate(EstudianteBase):
    """Modelo POO para actualización de un estudiante."""
    pass


class EstudianteResponse(EstudianteBase):
    """Modelo POO de respuesta que incluye el ID generado."""
    id: int