
# Disable certificate warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
import json


API_URL = 'https://t35nbzlj21.execute-api.us-east-1.amazonaws.com/produccion/users'

def get_users():
    response = requests.get(API_URL, timeout=2, verify=False)
    if response.status_code not in range(200, 301):
        raise RuntimeError('El codigo de error fue: ' + str(response.status_code))
    # Utilizo la funcion json() para devolver un diccionario dado que response es un Response object
    return response.json()

if __name__ == "__main__":
    print(get_users())