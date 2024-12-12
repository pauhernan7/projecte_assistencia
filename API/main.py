from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import date, time
from pydantic import BaseModel
from . import crud
from . import schemas
from typing import Optional
import logging
from fastapi.responses import Response


# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()



# Configuración CORS actualizada
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5502", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/{path:path}")
async def handle_preflight(path: str):
    return Response(status_code=200)

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

@app.get("/usuarios/{usuario_id}/estadisticas")
def obtener_estadisticas_usuario(usuario_id: int):
    resultado, error = crud.obtener_estadisticas_usuario(usuario_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return resultado

@app.get("/dashboard/")
def obtener_estadisticas_dashboard():
    try:
        logger.debug("Intentando obtener estadísticas del dashboard")
        resultado, error = crud.obtener_estadisticas_dashboard()
        if error:
            logger.error(f"Error al obtener estadísticas del dashboard: {error}")
            raise HTTPException(status_code=404, detail=error)
        logger.debug(f"Estadísticas obtenidas: {resultado}")
        return resultado
    except Exception as e:
        logger.exception("Error inesperado en /dashboard/")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/asistencias")
def obtener_asistencias():
    try:
        logger.debug("Intentando obtener asistencias")
        resultado, error = crud.obtener_asistencias()
        if error:
            logger.error(f"Error al obtener asistencias: {error}")
            raise HTTPException(status_code=404, detail=error)
        logger.debug(f"Asistencias obtenidas: {resultado}")
        return resultado
    except Exception as e:
        logger.exception("Error inesperado en /asistencias")
        raise HTTPException(status_code=500, detail=str(e))

class MateriaCreate(BaseModel):
    nombre: str
    grupo_id: int
    profesor_id: int

@app.post("/materias/")
def crear_materia(materia: MateriaCreate):
    resultado, error = crud.crear_materia(
        nombre=materia.nombre,
        grupo_id=materia.grupo_id,
        profesor_id=materia.profesor_id
    )
    if error:
        raise HTTPException(status_code=400, detail=error)
    return resultado

@app.get("/grupos/{grupo_id}/materias")
def obtener_materias(grupo_id: int):
    resultado, error = crud.obtener_materias_por_grupo(grupo_id)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return resultado

@app.get("/grupos/")
def obtener_grupos():
    resultado, error = crud.obtener_grupos()
    if error:
        raise HTTPException(status_code=400, detail=error)
    return resultado

