from sqlalchemy.orm import Session
from . import models, schemas

# Crear un nuevo usuario
def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Obtener un usuario por ID
def obtener_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

# Crear una nueva asistencia
def crear_asistencia(db: Session, asistencia: schemas.AsistenciaBase):
    db_asistencia = models.Asistencia(**asistencia.dict())
    db.add(db_asistencia)
    db.commit()
    db.refresh(db_asistencia)
    return db_asistencia