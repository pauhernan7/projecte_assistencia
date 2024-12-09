from pydantic import BaseModel, EmailStr
from datetime import datetime, time, date
from typing import Optional, Literal

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    rol: Literal["admin", "alumno", "profesor"]
    uid: str

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioResponse(UsuarioBase):
    id: int
    fecha_registro: datetime

    class Config:
        from_attributes = True

class AsistenciaBase(BaseModel):
    usuario_id: int
    fecha: date
    hora_entrada: time
    estado: Literal["presente", "ausente", "tarde"]
    hora_salida: Optional[time] = None

class AsistenciaResponse(BaseModel):
    id: int
    usuario_id: int
    fecha: date
    hora_entrada: time
    hora_salida: Optional[time]
    estado: str

    class Config:
        from_attributes = True

class AsistenciaActualizacion(BaseModel):
    hora_salida: time

class AsistenciaCreate(BaseModel):
    usuario_id: int
    estado: Literal["presente", "ausente", "tarde"]
    hora_entrada: Optional[time] = None  # Si no se proporciona, se usará la hora actual