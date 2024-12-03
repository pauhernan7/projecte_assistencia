from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class AsistenciaBase(BaseModel):
    usuario_id: int
    fecha: date
    hora_entrada: time
    estado: str
    hora_salida: time

class AsistenciaResponse(AsistenciaBase):
    id: int

    class Config:
        from_attributes = True