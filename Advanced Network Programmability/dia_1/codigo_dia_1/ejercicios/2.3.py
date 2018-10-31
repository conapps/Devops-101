
# Disable certificate warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
import json


API_URL = 'https://t35nbzlj21.execute-api.us-east-1.amazonaws.com/produccion/users'

def get_users():
    response = # Hacer request aqui
    status_code = response.status_code
    if status_code not in range(200, 300):
        raise RuntimeError('El codigo de error fue: ' + str(status_code))

    return # Devolver el diccionario de usuarios aqui

if __name__ == "__main__":
    print(get_users())