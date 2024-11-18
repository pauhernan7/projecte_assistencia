from fastapi import FastAPI,HTTPException
from typing import List
from pydantic import BaseModel

import db_aula 
import alumne
import db_alumne



app = FastAPI()

class alumnes(BaseModel):    
    IdAula: int
    nomAlumne: str
    cicle: str
    curs: str
    grup:  str


@app.get("/")
def read_root():
    return {"Students API"}


@app.get("/alumne/list", response_model=List[dict])  
def read_alumnes():
    
    pdb = db_alumne.read()

    alumnes_sch = alumne.alumnes_schema(pdb)

    return alumnes_sch

    return alumne.alumnes_schema(db_alumne.read())

