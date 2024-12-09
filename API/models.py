from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Enum, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    contraseña = Column(String(255))
    rol = Column(Enum("admin", "alumno", "profesor"))
    fecha_registro = Column(Date, server_default=func.current_date())
    uid = Column(String(50), unique=True, index=True)

class Asistencia(Base):
    __tablename__ = "asistencias"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha = Column(Date, default=func.current_date())
    hora_entrada = Column(Time, default=func.current_time())
    hora_salida = Column(Time, nullable=True)
    estado = Column(Enum("presente", "ausente", "tarde"))