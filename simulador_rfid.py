import requests
from datetime import datetime, date

# URL del endpoint de la API REST
URL_API = "http://localhost:8000/asistencias/"

# Simulación de datos del lector RFID
simulated_data = {
    "usuario_id": 1,
    "fecha": date.today().isoformat(),
    "hora_entrada": datetime.now().strftime("%H:%M:%S"),
    "estado": "presente",
    "hora_salida": datetime.now().strftime("%H:%M:%S")
}

# Configurar headers
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

try:
    print("Intentando enviar datos:", simulated_data)
    response = requests.post(URL_API, json=simulated_data, headers=headers)
    
    if response.status_code == 200:
        print("Datos enviados correctamente:")
        print(response.json())
    else:
        print(f"Error al enviar datos. Código de estado: {response.status_code}")
        print("Respuesta del servidor:", response.text)
except requests.exceptions.RequestException as e:
    print(f"Error al conectar con la API: {e}")