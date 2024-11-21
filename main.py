from awscrt import mqtt
from awsiot import mqtt_connection_builder
import time
import json
import pymysql

# Configuración de AWS IoT
ENDPOINT = "a202irx8mp4wwa-ats.iot.us-east-1.amazonaws.com"  # Tu endpoint MQTT
CLIENT_ID = "mi_dispositivo"         # Identificador único para tu dispositivo
TOPIC = "esp32/data"                 # Topic al que te suscribirás
CERTIFICATE_PATH = "certificats/certificate.pem.crt"
PRIVATE_KEY_PATH = "certificats/private.pem.key"
CA_PATH = "certificats/AmazonRootCA1.pem"

# Configuración de MySQL
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "tu_password"
DB_NAME = "proyecte_gestio_assistencia"

# Callback para cuando se recibe un mensaje
def on_message_received(topic, payload, **kwargs):
    print(f"Mensaje recibido en el topic '{topic}': {payload.decode()}")
    # Procesar el mensaje y guardarlo en la base de datos
    try:
        data = json.loads(payload)
        insertar_en_base_de_datos(data)
    except Exception as e:
        print(f"Error procesando el mensaje: {e}")

# Conectar a la base de datos y guardar datos
def insertar_en_base_de_datos(data):
    try:
        conexion = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        with conexion.cursor() as cursor:
            query = """
                INSERT INTO Asistencias (usuario_id, fecha, hora_entrada, estado)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (data['usuario_id'], data['fecha'], data['hora_entrada'], data['estado']))
            conexion.commit()
        print("Datos insertados correctamente en la base de datos.")
    except Exception as e:
        print(f"Error insertando en la base de datos: {e}")
    finally:
        conexion.close()

# Crear conexión MQTT
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=CERTIFICATE_PATH,
    pri_key_filepath=PRIVATE_KEY_PATH,
    ca_filepath=CA_PATH,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30,
)

print(f"Conectando al endpoint {ENDPOINT} con ID '{CLIENT_ID}'...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("¡Conectado a AWS IoT!")

# Suscribirse al topic
print(f"Suscribiéndose al topic '{TOPIC}'...")
subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=TOPIC,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received
)
subscribe_future.result()
print(f"Suscripción al topic '{TOPIC}' completada.")

# Mantener la conexión activa
try:
    print("Esperando mensajes (Ctrl+C para salir)...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Desconectando...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Desconectado.")