
# Disable certificate warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
import json

from conatel import send_message, delete_users, get_hostname
from cli import configure

API_URL = 'https://t35nbzlj21.execute-api.us-east-1.amazonaws.com/produccion/users'
USER_KEY = 'YjYxNTljMjEtZWMxNS00MDkyLThhODAtODA3ODgyYzUwOTM3ZjhjNzdlZDUtM2Fi'

def get_users():
    response = requests.get(API_URL, timeout=2, verify=False)
    if response.status_code not in range(200, 301):
        raise RuntimeError('El codigo de error fue: ' + str(response.status_code))
    # Utilizo la funcion json() para devolver un diccionario dado que response es un Response object
    return response.json()

try:
    users = get_users()
    delete_users()
    for user in users['users']:
        command = 'username ' + user['username'] + ' privilege ' + str(user['level']) + ' secret ' + user['password']
        configure(command)
    send_message('Usuarios locales actualizados correctamente en el router ' + get_hostname(), USER_KEY)
except Exception as error:
    print('Error al actualizar los usuarios:\n' + str(error))
    send_message('Error al actualizar los usuarios:\n' + str(error), USER_KEY)
