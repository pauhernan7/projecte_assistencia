from fastapi import FastAPI, HTTPException
from datetime import date, time
from . import crud
from . import schemas

app = FastAPI()

@app.post("/usuarios/", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate):
    resultado, error = crud.crear_usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        contraseña=usuario.contraseña,
        rol=usuario.rol,
        uid=usuario.uid
    )
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    return resultado

@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def obtener_usuario(usuario_id: int):
    resultado, error = crud.obtener_usuario(usuario_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return resultado

@app.post("/asistencias/", response_model=schemas.AsistenciaResponse)
def crear_asistencia(asistencia: schemas.AsistenciaCreate):
    resultado, error = crud.crear_asistencia(
        usuario_id=asistencia.usuario_id,
        estado=asistencia.estado,
        hora_entrada=asistencia.hora_entrada
    )
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    return resultado

@app.get("/usuarios/{usuario_id}/asistencias", response_model=list[schemas.AsistenciaResponse])
def obtener_asistencias_usuario(usuario_id: int):
    resultado, error = crud.obtener_asistencias_usuario(usuario_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return resultado