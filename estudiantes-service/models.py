from pydantic import BaseModel, EmailStr, Field

class EstudianteCreate(BaseModel):
    codigo: str = Field(..., min_length=3, max_length=20)
    nombres: str = Field(..., min_length=2, max_length=100)
    apellidos: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr
    carrera: str = Field(..., min_length=3, max_length=100)

class EstudianteUpdate(BaseModel):
    codigo: str = Field(..., min_length=3, max_length=20)
    nombres: str = Field(..., min_length=2, max_length=100)
    apellidos: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr
    carrera: str = Field(..., min_length=3, max_length=100)

class EstudianteResponse(BaseModel):
    id: int
    codigo: str
    nombres: str
    apellidos: str
    correo: str
    carrera: str
