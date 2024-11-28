from fastapi import FastAPI,HTTPException, File, UploadFile
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


import usuari
import db_usuari



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class tablaAlumne(BaseModel):
    NomAlumne: str
    cicle: str
    curs: str
    grup: str
    descAula: str


@app.get("/")
def read_root():
    return {"message": "Students API"}


@app.get("/usuaris/llista")
def read_alumnes():
    usuaris_list = db_usuari.read()
    return usuari.usuaris_schema(usuaris_list)


""" @app.get("/alumnes/list", response_model=List[tablaAlumne])
def read_alumnes(orderby: str | None = None,  contain: str | None = None, skip: int = 0, limit: int | None = None ):
    
    alumnes_list = db_alumne.read(orderby=orderby, contain=contain, skip=skip, limit=limit)

    if not alumnes_list:
        raise HTTPException(status_code=404, detail="No s'han trobat alumnes")
    return alumne.alumnes_schema(alumnes_list)

@app.post("/alumne/loadAlumnes")
async def load_alumnes(file: UploadFile = File(...)):
    resultat = db_alumne.alumnesCSV(file)   
    return resultat """


