"""
Script #12 - Spark mission.
"""

import sys
import json
import requests

# 1. Agregar el token personal de desarrollador de Spark.
TOKEN = None
# 2. Agregar el nombre del room donde se escribirán los mensajes.
ROOM_NAME = None
# 3. Escribir el mensaje que será públicado en el grupo.
MESSAGE = None

def get_headers():
    """ Devuelve un diccionario con los encabezados necesarios. """
    return {
        "Authorization": "Bearer " + TOKEN,
        "Content-Type": "application/json; charset=utf-8"
    }

def find_room_id(room_name):
    """ Encuentra la id de un room a partir de su nombre. """
    room_id = None
    url = "https://webexapis.com/v1/rooms"
    response = requests.get(url, headers=get_headers(), verify=False)
    json_response = response.json()
    for room in json_response["items"]:
        if room["title"] == room_name:
            print("\nFound room: ", room)
            # 4. Modifique la siguiente linea para almacenar la id del room en
            # la variable room_id
            room_id = None
            break # Este operando permite salir de un for-loop antes de terminar
    return room_id

def create_room(room_name):
    """ Crea un nuevo room si este no existe actualmente. """
    room_id = find_room_id(room_name)
    if room_id is None:
        data = {"title": room_name}
        url = "https://webexapis.com/v1/rooms"
        response = requests.post(url, json=data, headers=get_headers())
        json_response = response.json()
        print("\nCreated room:", json_response)
        # 5. Modifique la siguiente linea para almacenar la id del room creado 
        # en la variable room_id
        room_id = None
    return room_id

def add_test_member(room_id):
    """ Agrega un usuario de prueba a un grupo. """
    data = {
        "roomId": room_id,
        "personEmail": "test@test.com",
        "isModerator": False
    }
    url = "https://webexapis.com/v1/memberships"
    response = requests.post(url, json=data, headers=get_headers())
    print("\nAdded test member:", response.json())

def post_message(room_id, message):
    """ Publica un mensaje en el room indicado. """
    data = {
        "roomId": room_id,
        "text": message
    }
    url = "https://webexapis.com/v1/messages"
    response = requests.post(url, json=data, headers=get_headers())
    print("\nPosted message:", response.json())

def get_room_info(room_id):
    """ Gets the room details """
    # 6. Investiga en la documentación de Spark para hallar la URL necesaria 
    # para obtener los detalles de un room.
    url = None
    if url is None:
        sys.exit("Por favor agregue la url para obtener los detalle de un room")
    response = requests.get(url, headers=get_headers())
    json_response = response.json()
    # 7. Imprima los detalles del room de forma que sea fácil de leer JSON.

# Este bloque permite que los comandos expresados a continuación solo se
# correrán cuando el script es invocado desde la consola, pero no is es
# importado desde otro módulo.
if __name__ == '__main__':
    if TOKEN is None or ROOM_NAME is None or MESSAGE is None:
        sys.exit("Verifique que las constantes estén correctamente \
configuradas.")
    # Obtenemos el id del room de interes.
    ROOM_ID = create_room(ROOM_NAME)
    if ROOM_ID is None:
        sys.exit("Verifique que las funciones get_room y create_room devuelvan \
el room_id correctamente.")
    # Agregamos un miembro de prueba.
    add_test_member(ROOM_ID)
    # Posteamos un mensaje en el room.
    post_message(ROOM_ID, MESSAGE)
    # Obtenemos los detalles del room.
    get_room_info(ROOM_ID)
