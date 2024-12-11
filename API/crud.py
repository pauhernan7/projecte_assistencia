from datetime import date, time, datetime, timedelta
import mysql.connector
from .database import conectar_db, cerrar_conexion
from typing import Optional, Tuple, Dict, Any

def crear_usuario(nombre: str, apellido: str, email: str, contraseña: str, rol: str, uid: str):
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            
            # Verificaciones de unicidad
            if _existe_email(cursor, email):
                return None, "El email ya está registrado"
            if _existe_uid(cursor, uid):
                return None, "El UID ya está registrado"

            # Insertar usuario
            sql = """
            INSERT INTO usuarios (nombre, apellido, email, contraseña, rol, uid)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, apellido, email, contraseña, rol, uid))
            conexion.commit()
            
            # Obtener el usuario recién creado
            nuevo_id = cursor.lastrowid
            return obtener_usuario(nuevo_id)[0], None

        except Exception as e:
            return None, f"Error al crear usuario: {str(e)}"
        finally:
            cerrar_conexion(conexion)
    return None, "Error de conexión a la base de datos"

# Funciones auxiliares para verificaciones
def _existe_email(cursor, email: str) -> bool:
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    return cursor.fetchone() is not None

def _existe_uid(cursor, uid: str) -> bool:
    cursor.execute("SELECT id FROM usuarios WHERE uid = %s", (uid,))
    return cursor.fetchone() is not None

def obtener_usuario(usuario_id: int):
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id, nombre, apellido, email, rol, uid, fecha_registro 
                FROM usuarios 
                WHERE id = %s
            """, (usuario_id,))
            
            usuario = cursor.fetchone()
            if usuario:
                return {
                    "id": usuario[0],
                    "nombre": usuario[1],
                    "apellido": usuario[2],
                    "email": usuario[3],
                    "rol": usuario[4],
                    "uid": usuario[5],
                    "fecha_registro": usuario[6]
                }, None
            return None, "Usuario no encontrado"
            
        except Exception as e:
            return None, str(e)
        finally:
            cerrar_conexion(conexion)
    return None, "Error de conexión a la base de datos"

def crear_asistencia(usuario_id: int, estado: str, hora_entrada: Optional[time] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            
            # Verificar si el usuario existe
            cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
            if not cursor.fetchone():
                return None, "Usuario no encontrado"

            # Verificar si ya existe una asistencia para hoy
            cursor.execute("""
                SELECT id FROM asistencias 
                WHERE usuario_id = %s AND fecha = CURRENT_DATE()
            """, (usuario_id,))
            if cursor.fetchone():
                return None, "Ya existe una asistencia registrada hoy para este usuario"

            # Insertar asistencia
            sql = """
            INSERT INTO asistencias (usuario_id, fecha, hora_entrada, estado)
            VALUES (%s, CURRENT_DATE(), COALESCE(%s, CURRENT_TIME()), %s)
            """
            cursor.execute(sql, (usuario_id, hora_entrada, estado))
            conexion.commit()
            
            # Obtener la asistencia creada con manejo de errores mejorado
            nuevo_id = cursor.lastrowid
            asistencia, error = obtener_asistencia(nuevo_id)
            if error:
                print(f"Error al obtener la asistencia creada: {error}")  # Debug
                return None, f"La asistencia se creó pero hubo un error al recuperarla: {error}"
            return asistencia, None

        except Exception as e:
            print(f"Error en crear_asistencia: {str(e)}")  # Debug
            return None, f"Error al crear asistencia: {str(e)}"
        finally:
            cerrar_conexion(conexion)
    return None, "Error de conexión a la base de datos"

def obtener_asistencia(asistencia_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.*, u.nombre, u.apellido 
                FROM asistencias a
                JOIN usuarios u ON a.usuario_id = u.id
                WHERE a.id = %s
            """, (asistencia_id,))
            
            asistencia = cursor.fetchone()
            if asistencia:
                # Convertir timedelta a time
                if isinstance(asistencia["hora_entrada"], timedelta):
                    asistencia["hora_entrada"] = (datetime.min + asistencia["hora_entrada"]).time()
                if asistencia["hora_salida"] and isinstance(asistencia["hora_salida"], timedelta):
                    asistencia["hora_salida"] = (datetime.min + asistencia["hora_salida"]).time()
                
                # Construir respuesta con el formato correcto
                return {
                    "id": asistencia["id"],
                    "usuario_id": asistencia["usuario_id"],
                    "fecha": asistencia["fecha"],
                    "hora_entrada": asistencia["hora_entrada"],
                    "hora_salida": asistencia["hora_salida"],
                    "estado": asistencia["estado"]
                }, None
            return None, "Asistencia no encontrada"
            
        except Exception as e:
            print(f"Error en obtener_asistencia: {str(e)}")  # Debug
            return None, f"Error en la base de datos: {str(e)}"
        finally:
            cerrar_conexion(conexion)
    return None, "Error de conexión a la base de datos"

def obtener_asistencias_usuario(usuario_id: int) -> Tuple[Optional[list], Optional[str]]:
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.*, u.nombre, u.apellido 
                FROM asistencias a
                JOIN usuarios u ON a.usuario_id = u.id
                WHERE a.usuario_id = %s
                ORDER BY a.fecha DESC, a.hora_entrada DESC
            """, (usuario_id,))
            
            asistencias = cursor.fetchall()
            if asistencias:
                # Convertir timedelta a time para cada asistencia
                for asistencia in asistencias:
                    if isinstance(asistencia["hora_entrada"], timedelta):
                        asistencia["hora_entrada"] = (datetime.min + asistencia["hora_entrada"]).time()
                    if asistencia["hora_salida"] and isinstance(asistencia["hora_salida"], timedelta):
                        asistencia["hora_salida"] = (datetime.min + asistencia["hora_salida"]).time()
                
                return asistencias, None
            return [], None  # Devolvemos lista vacía en lugar de None cuando no hay asistencias
            
        except Exception as e:
            print(f"Error en obtener_asistencias_usuario: {str(e)}")  # Debug
            return None, str(e)
        finally:
            cerrar_conexion(conexion)
    return None, "Error de conexión a la base de datos"

def obtener_estadisticas_usuario(usuario_id: int):
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            
            # Verificar si el usuario existe
            cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
            if not cursor.fetchone():
                return None, "Usuario no encontrado"

            # Obtener estadísticas
            sql = """
            SELECT 
                COUNT(*) as total_registros,
                SUM(CASE WHEN estado = 'presente' THEN 1 ELSE 0 END) as total_presente,
                SUM(CASE WHEN estado = 'ausente' THEN 1 ELSE 0 END) as total_ausente,
                SUM(CASE WHEN estado = 'tarde' THEN 1 ELSE 0 END) as total_tarde
            FROM asistencias 
            WHERE usuario_id = %s
            """
            cursor.execute(sql, (usuario_id,))
            stats = cursor.fetchone()
            
            if stats and stats['total_registros'] > 0:
                porcentaje = round((stats['total_presente'] / stats['total_registros']) * 100, 2)
                return {
                    "usuario_id": usuario_id,
                    "porcentaje_asistencia": porcentaje,
                    "total_presente": stats['total_presente'],
                    "total_ausente": stats['total_ausente'],
                    "total_tarde": stats['total_tarde']
                }, None
            return {
                "usuario_id": usuario_id,
                "porcentaje_asistencia": 0,
                "total_presente": 0,
                "total_ausente": 0,
                "total_tarde": 0
            }, None
            
        except Exception as e:
            print(f"Error en obtener_estadisticas: {str(e)}")  # Debug
            return None, f"Error en la base de datos: {str(e)}"
        finally:
            cerrar_conexion(conexion)
    return None, "Error de conexión a la base de datos"

def crear_materia(nombre: str, grupo_id: int, profesor_id: int):
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)

            # Verificar si el grupo existe
            cursor.execute("SELECT id FROM grupos WHERE id = %s", (grupo_id,))
            if not cursor.fetchone():
                return None, "Grupo no encontrado"

            # Verificar si el profesor existe y es profesor
            cursor.execute("""
                SELECT id FROM usuarios 
                WHERE id = %s AND rol = 'profesor'
            """, (profesor_id,))
            if not cursor.fetchone():
                return None, "Profesor no encontrado o el usuario no es profesor"

            # Insertar la materia
            cursor.execute("""
                INSERT INTO materias (nombre, grupo_id, profesor_id)
                VALUES (%s, %s, %s)
            """, (nombre, grupo_id, profesor_id))
            conexion.commit()
            
            nuevo_id = cursor.lastrowid
            return {"id": nuevo_id, "nombre": nombre, "grupo_id": grupo_id, "profesor_id": profesor_id}, None

        except Exception as e:
            return None, f"Error al crear materia: {str(e)}"
        finally:
            cerrar_conexion(conexion)
    return None, "Error de conexión a la base de datos"

def obtener_materias_por_grupo(grupo_id: int):
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT m.*, u.nombre as profesor_nombre, g.nombre as grupo_nombre
                FROM materias m
                JOIN usuarios u ON m.profesor_id = u.id
                JOIN grupos g ON m.grupo_id = g.id
                WHERE m.grupo_id = %s
            """, (grupo_id,))
            materias = cursor.fetchall()
            return materias, None
        except Exception as e:
            return None, f"Error al obtener materias: {str(e)}"
        finally:
            cerrar_conexion(conexion)
    return None, "Error de conexión a la base de datos"

def obtener_grupos():
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM grupos ORDER BY nombre")
            grupos = cursor.fetchall()
            return grupos, None
        except Exception as e:
            return None, f"Error al obtener grupos: {str(e)}"
        finally:
            cerrar_conexion(conexion)
    return None, "Error de conexión a la base de datos"

def obtener_estadisticas_dashboard():
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            
            # Obtener total de usuarios
            cursor.execute("SELECT COUNT(*) as total FROM usuarios")
            total_usuarios = cursor.fetchone()['total']
            
            # Obtener total de asistencias
            cursor.execute("SELECT COUNT(*) as total FROM asistencias")
            total_asistencias = cursor.fetchone()['total']
            
            # Obtener total de materias
            cursor.execute("SELECT COUNT(*) as total FROM materias")
            total_materias = cursor.fetchone()['total']
            
            # Calcular porcentaje de asistencia
            cursor.execute("""
                SELECT 
                    (COUNT(CASE WHEN estado = 'presente' THEN 1 END) * 100.0 / COUNT(*)) as porcentaje
                FROM asistencias
            """)
            porcentaje = cursor.fetchone()['porcentaje'] or 0
            
            return {
                "total_usuarios": total_usuarios,
                "total_asistencias": total_asistencias,
                "total_materias": total_materias,
                "porcentaje_asistencia": round(porcentaje, 2)
            }, None
            
        except Exception as e:
            print(f"Error en obtener_estadisticas_dashboard: {str(e)}")
            return None, f"Error al obtener estadísticas: {str(e)}"
        finally:
            cerrar_conexion(conexion)
    return None, "Error de conexión a la base de datos"

def obtener_asistencias():
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.*, u.nombre, u.apellido
                FROM asistencias a
                JOIN usuarios u ON a.usuario_id = u.id
                ORDER BY a.fecha DESC, a.hora_entrada DESC
                LIMIT 50
            """)
            asistencias = cursor.fetchall()
            return asistencias, None
        except Exception as e:
            print(f"Error en obtener_asistencias: {str(e)}")
            return None, f"Error al obtener asistencias: {str(e)}"
        finally:
            cerrar_conexion(conexion)
    return None, "Error de conexión a la base de datos"