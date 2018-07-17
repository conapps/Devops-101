"""
Script #14 - APIC-EM and Spark mission.
"""

import sys
import json
import requests

# Disable warnings
requests.packages.urllib3.disable_warnings()

# 1. Ingresar la URL de la API del APIC-EM
CONTROLLER = "https://devnetapi.cisco.com/sandbox/apic_em/api/v1"
# 2. Ingresar el token de desarrollador de Spark.
TOKEN = "YmU3OTE3NTAtMzU1ZS00NjBmLTg4MDMtYmMyMjAxNzY3NTkyZWE0ZjJlODMtMzRh"
# URL de la API de Spark.
SPARK_URL = "https://api.ciscospark.com/v1"

# ----------------
# Helper functions
# ----------------
def table_headers(printed):
    """ Format and print table headers """
    result = (
        '\n{:>10}'.format("Source")
        + '{:>30}'.format("Source Interface")
        + '{:>25}'.format("Target Interface")
        + '{:>13}'.format("Status")
    )
    if printed == 1:
        print()
    print(result)
    return result

def node_link(node, link):
    """ Format and print a node link """
    result = (
        "    "
        + '{:<20}'.format(node["label"])
        + '{:<25}'.format(link["startPortName"])
        + '{:<23}'.format(link["endPortName"])
        + '{:<8}'.format(link["linkStatus"])
    )
    print(result)
    return result

def unkown_link(node, link):
    """ Format and print an unknown link """
    result = (
        "    "
        + '{:<20}'.format(node["label"])
        + '{:<25}'.format("unknown")
        + '{:<23}'.format("unknown")
        + '{:<8}'.format(link["linkStatus"])
    )
    print(result)
    return result

# --------------
# Main functions
# --------------
def get_ticket():
    """ Gets a valid ticket from the APIC-EM """
    # 3. Configurar el nombre de usuario del APIC-EM.
    username = "devnetuser"
    # 4. Configurar la contraseña del usuario del APIC-EM.
    password = "Cisco123!"

    if CONTROLLER is None or username is None or password is None:
        sys.exit("Por favor asigna los valores correctos a la constante\
CONTROLLER y configura correctamente las credenciales.")

    endpoint = "/ticket"
    url = CONTROLLER + endpoint
    payload = json.dumps({
        "username": username,
        "password": password
    })
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=payload, headers=headers, verify=False)
    json_response = response.json()
    # 5. Tomar el service ticket de la respuesta.
    ticket = json_response["response"]["serviceTicket"]
    return ticket

def get_topology():
    """ Gets the physical topology from the APIC-EM """
    result = []
    # 6. Definir el endpoint necesario para obtener la topología física.
    endpoint = "/topology/physical-topology"

    if endpoint is None:
        sys.exit("Por favor configure el `endpoint` correcto para obtener \
información sobre la topología física.")

    url = CONTROLLER + endpoint
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": get_ticket()
    }
    json_response = requests.get(url, headers=headers, verify=False).json()
    # Los siguientes loops recorren la arquitectura de la toplogía física
    # y almacenan el resultado en la lista `result` definida anteriormente.
    for node in json_response["response"]["nodes"]:
        found = 0    # print header flag
        printed = 0  # formatting flag
        for link in json_response["response"]["links"]:
            # Find interfaces that link to this one which means this node is
            # the target.
            if link["target"] == node["id"]:
                if found == 0:
                    result.append(table_headers(printed))
                    found = 1
                for other_node in json_response["response"]["nodes"]:
                    # find name of node to that connects to this one
                    if link["source"] == other_node["id"]:
                        if "startPortName" in link:
                            result.append(node_link(other_node, link))
                        else:
                            result.append(unkown_link(other_node, link))
                        break
    return result

def get_room_id():
    """ Gets a spark room id. """
    endpoint = "/rooms"

    if TOKEN is None:
        sys.exit("Por favor configure su token de desarrollador para Spark.")

    url = SPARK_URL + endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + TOKEN
    }
    json_response = requests.get(url, headers=headers, verify=False).json()

    for item in json_response["items"]:
        title = item["title"]
        title = title.encode("ascii", errors="backslashreplace")
        title = title.decode("ascii")
        print("\nTitle:", title)
        print("Room ID", item["id"], end="\n\n")
        user_input = input("Is this the room you are looking for? [y/n] ")
        if user_input.lower() == "y" or user_input.lower() == "yes":
            print("\nGot it!")
            return item["id"]
        else:
            continue

def post_spark(text, room_id):
    """ Posts a message to the corresponding room. """
    endpoint = "/messages"
    url = SPARK_URL + endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + TOKEN
    }
    data = json.dumps({
        "roomId": room_id,
        "text": "\n".join(text)
    })
    requests.post(url, data=data, headers=headers, verify=False)
    print("\nCheck the Spark room to see if your message was posted.")

if __name__ == "__main__":
    # El mensaje será la topología física almacenada en el APIC-EM
    MESSAGE = get_topology()

    # Ahora debemos obtener el id del `room` al que queremos imprimir.
    ROOM_ID = get_room_id()

    # Por último tenemos que posteaer el mensaje en el `room` de Spark.
    post_spark(MESSAGE, ROOM_ID)
