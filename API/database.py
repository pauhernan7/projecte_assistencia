import mysql.connector
from mysql.connector import Error

def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="system",
            database="projecte_assistencia",
            auth_plugin='mysql_native_password'
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion
        return None
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def cerrar_conexion(conexion):
    if conexion and conexion.is_connected():
        conexion.close()
        print("Conexión cerrada")