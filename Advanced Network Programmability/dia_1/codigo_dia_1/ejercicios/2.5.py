
# Disable certificate warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
import json

from conatel import send_message, delete_users, get_hostname
from cli import configure

API_URL = 'https://t35nbzlj21.execute-api.us-east-1.amazonaws.com/produccion/users'
USER_KEY = # completar con la clave de desarrollador de Webex Teams

def get_users():
    response = requests.get(API_URL, timeout=2, verify=False)
    if response.status_code not in range(200, 301):
        raise RuntimeError('El codigo de error fue: ' + str(response.status_code))
    # Utilizo la funcion json() para devolver un diccionario dado que response es un Response object
    return response.json()

try:
    users = # 1) traer usuarios a configurar desde la API

    # 2) Borrar los usuarios actuales aqui

    for user in users['users']:
        command = # 3) escribir el comando
        configure(command)

    mensaje = 'Usuarios locales actualizados correctamente en el router ' + get_hostname()
    # 4) Enviar mensaje al grupo de Teams indicando el exito o fracaso de la operacion, utilizar funcion send_message()

except Exception as error:
    print('Error al actualizar los usuarios:\n' + str(error))
    send_message('Error al actualizar los usuarios:\n' + str(error), USER_KEY)
