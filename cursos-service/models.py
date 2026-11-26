from pydantic import BaseModel, Field

class CursoCreate(BaseModel):
    codigo: str = Field(..., min_length=3, max_length=20)
    nombre: str = Field(..., min_length=3, max_length=120)
    creditos: int = Field(..., ge=1, le=10)
    docente: str = Field(..., min_length=3, max_length=120)

class CursoUpdate(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=120)
    creditos: int = Field(..., ge=1, le=10)
    docente: str = Field(..., min_length=3, max_length=120)

class CursoResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    creditos: int
    docente: str
