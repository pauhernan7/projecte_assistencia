from pydantic import BaseModel
from typing import Optional, Literal

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    rol: Literal['alumno', 'admin', 'profesor']  # Solo acepta estos valores
    uid: str

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        orm_mode = True

class AsistenciaBase(BaseModel):
    usuario_id: int
    fecha: str
    hora_entrada: str
    estado: str

class AsistenciaResponse(AsistenciaBase):
    id: int

    class Config:
        orm_mode = True