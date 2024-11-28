import csv
import io
from client import db_client
from fastapi import UploadFile

def read():
    try:
        # Conexión a la base de datos
        conn = db_client()
        cur = conn.cursor()

        # Consulta simple para obtener todos los usuarios
        query = "SELECT * FROM usuarios"

        # Ejecutar la consulta
        cur.execute(query)
        
        # Obtener todos los resultados
        usuaris = cur.fetchall()

    except Exception as e:
        return {"status": -1, "message": f"{e}"}
    
    finally:
        # Cerrar la conexión y el cursor
        if cur: cur.close()
        if conn: conn.close()
    
    return usuaris

