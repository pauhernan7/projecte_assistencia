from sqlalchemy.orm import Session
from . import models, schemas

def crear_asistencia(db: Session, asistencia: schemas.AsistenciaBase):
    db_asistencia = models.Asistencia(**asistencia.dict())
    db.add(db_asistencia)
    db.commit()
    db.refresh(db_asistencia)
    return db_asistencia

def obtener_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()