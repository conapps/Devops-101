import requests
import sys
import json

#UMBRAL = int(sys.argv[1])
UMBRAL = 000000
MERAKI_KEY = "fbabc72a20a98eed4ed736d035b7b12b44c21b76"
ORG_NAME = 'C008 - Preventa Conatel'
NETWORK_NAME = 'W001 - Wireless ACME'

api_meraki = "https://dashboard.meraki.com/api/v0/"
spark_room_name_test = 'Milagro'
spark_key = 'NmY4ZTg2YjUtMzRmNy00Y2ZjLTkwOTYtNzYyODBlM2EyNTkzYjdiZDIwOTgtZTkz'
api_spark = 'https://api.ciscospark.com/v1'


def get_organization_id(key, name):
    """Función que toma como argumento la key del usuario y el nombre de la organizacion y devuelve
    la key de la organizacion
    """
    endpoint = "organizations"
    url = api_meraki + endpoint

    headers = {
        'x-cisco-meraki-api-key': key,
        'content-type': "application/json",
        }

    response = requests.request("GET", url, headers=headers).json()
    for organization in response:
        if organization['name'] == name:
            return organization['id']


def get_network_id(org_id, key, name):
    """Función que toma como argumento la key del usuario, el ID de la organización y el nombre de la red
    y devuelve el id de la red
    """
    endpoint = 'organizations/' + str(org_id) + '/networks'
    url = api_meraki + endpoint

    headers = {
        'x-cisco-meraki-api-key': key,
        'content-type': "application/json",
        }

    response = requests.request("GET", url, headers=headers).json()
    for red in response:
        if red['name'] == name:
            return red['id']


def get_traffic(netw_id, key):
    """Función que toma como argumento la key del usuario y el ID de la red
    y devuelve una lista con todo el tráfico de dicha red
    """
    endpoint = 'networks/' + netw_id + '/traffic'
    url = api_meraki + endpoint

    querystring = {"timespan": "2592000"}

    headers = {
        'x-cisco-meraki-api-key': key,
        'content-type': "application/json",
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()


def get_room_id(key, room_name):
    url = api_spark + '/rooms'

    headers = {
        'authorization': "Bearer " + key,
        'content-type': "application/json",
    }

    response = requests.request("GET", url, headers=headers).json()
    print(response)
    for room, value in response.items():
        print(value)
        for item in value:
            if item['title'] == room_name:
                return item['id']


def post_message(key, sala_id, text):
    url = api_spark + '/messages'

    headers = {
        'authorization': "Bearer " + key,
        'content-type': "application/json",
    }

    payload = {
        "roomId": sala_id,
        "markdown": text
    }

    payload = json.dumps(payload)

    return requests.request("POST", url, data=payload, headers=headers).json()

org_id = get_organization_id(MERAKI_KEY, ORG_NAME)
print('El org_id es:', org_id)
net_id = get_network_id(org_id, MERAKI_KEY, NETWORK_NAME)
print('El netw_id es: ', net_id)
trafico = get_traffic(net_id, MERAKI_KEY)

mensaje = 'Aplicaciones con mas de ' + str(UMBRAL) + 'B.'
mensaje += '\n===\n'
for app in trafico:
    enviado = int(app['sent'])
    recibido = int(app['recv'])
    if enviado + recibido > UMBRAL:
        mensaje += '\n'
        mensaje += '**' + app['application'] + '**' + '\n'
        mensaje += '\tEnviado:' + str(app['sent']) + '\n'
        mensaje += '\tRecibido:' + str(app['recv']) + '\n'
        mensaje += '\tTotal:' + str(enviado + recibido) + '\n'

room_id = get_room_id(spark_key, spark_room_name_test)
print('El id de la sala es: ', room_id)
post = post_message(spark_key, room_id, mensaje)
print('El mensaje posteado fue: ', post['markdown'])

