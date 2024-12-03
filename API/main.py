from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, Base, get_db
from typing import List
from datetime import datetime, time

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/asistencias/", response_model=schemas.AsistenciaResponse)
def crear_asistencia(asistencia: schemas.AsistenciaBase, db: Session = Depends(get_db)):
    try:
        # Verificar si el usuario existe
        usuario = crud.obtener_usuario(db, asistencia.usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return crud.crear_asistencia(db, asistencia)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))