"""
Script #11 - First python-spark api call
"""

import json
import requests

TOKEN = # Ingrese su clave de desarrollador de SPARK aqui.

def get_headers():
    """ Devuelve un diccionario con los encabezados necesarios. """
    return {
        "Authorization": "Bearer " + TOKEN,
        "Content-Type": "application/json; charset=utf-8"
    }

def get_rooms():
    """ Llama al endpoint /rooms """
    url = "https://api.ciscospark.com/v1/rooms"
    response = requests.get(url, headers=get_headers())
    return response.json()

ROOMS = get_rooms()

print('Spark response data:')
# Format output to make it easier to read.
print(json.dumps(ROOMS, indent=4, separators=(',', ':')))
