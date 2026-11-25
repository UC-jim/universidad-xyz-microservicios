from pydantic import BaseModel, Field


class CursoBase(BaseModel):
    codigo: str = Field(..., min_length=3, max_length=20, example="CUR101")
    nombre: str = Field(..., min_length=3, max_length=120, example="Arquitectura de Software")
    creditos: int = Field(..., ge=1, le=10, example=4)
    docente: str = Field(..., min_length=3, max_length=120, example="Dr. Carlos Mendoza")


class CursoCreate(CursoBase):
    """Modelo POO para creación de un curso."""
    pass


class CursoUpdate(CursoBase):
    """Modelo POO para actualización de un curso."""
    pass


class CursoResponse(CursoBase):
    """Modelo POO de respuesta que incluye el ID generado."""
    id: int