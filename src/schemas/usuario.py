
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from datetime import datetime
from src.enums import RolGlobal


class UsuarioCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    @field_validator("username")
    @classmethod
    def username_correcto(cls, v: str) -> str:
        if " " in v or "@" in v:
            raise ValueError("El nombre de usuario no puede contener espacios ni '@' especiales")
        return v
    
    nombre: str = Field(min_length=2, max_length=100)
    apellidos: str = Field(min_length=2, max_length=100)
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=8, max_length=72)
    telefono: str | None = Field(default=None, max_length=20)

class UsuarioRead(BaseModel):
    id: int
    username: str
    nombre: str
    apellidos: str
    email: EmailStr
    rol: RolGlobal
    fecha_alta: datetime
    activo: bool
    telefono: str | None = None
    model_config = ConfigDict(from_attributes=True)