
# Disable certificate warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
import json

from dia_1.codigo_dia_1.lib.conatel import send_message

API_URL = 'https://t35nbzlj21.execute-api.us-east-1.amazonaws.com/produccion/users'
USER_KEY = 'YjYxNTljMjEtZWMxNS00MDkyLThhODAtODA3ODgyYzUwOTM3ZjhjNzdlZDUtM2Fi'

def get_users():
    response = requests.get(API_URL, timeout=2, verify=False)
    if response.status_code not in range(200, 301):
        raise RuntimeError('El codigo de error fue: ' + str(response.status_code))
    # Utilizo la funcion json() para devolver un diccionario dado que response es un Response object
    return response.json()

users = get_users()

mensaje = {
    'usuarios': []
}

i = 0
for user in users['users']:
    mensaje['usuarios'].append(user)
    i += 1
    if i == 3:
        break

send_message(json.dumps(mensaje, indent=2), USER_KEY)