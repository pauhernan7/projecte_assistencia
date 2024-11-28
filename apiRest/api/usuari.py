def usuari_schema(fetchUsuari) -> dict:
    return {
        "usuario_id": fetchUsuari[0],
        "nombre": fetchUsuari[1],
        "apellido": fetchUsuari[2],
        "email": fetchUsuari[3],
        "rol": fetchUsuari[4]
    }

    
def usuaris_schema(fetchUsuaris) -> dict:
    return [usuari_schema(fetchUsuari) for fetchUsuari in fetchUsuaris]




