import requests
import sys

# Constante que contiene el umbral de tráfico en Bytes
UMBRAL = int(sys.argv[1])

# Constante que contiene el lapso de tiempo que hay que medir (un mes) medido en segundos
TIME_SPAN = 2592000

# Clave para poder autenticar con la API de Meraki
MERAKI_KEY = "fbabc72a20a98eed4ed736d035b7b12b44c21b76"

# Nombre de la organización en Meraki que contiene la red para la cuál hay que obtener estadísticas
ORG_NAME = 'C008 - Preventa Conatel'

# Nombre de la red para cuál hay que obtener estadísticas
NETWORK_NAME = 'W001 - Wireless ACME'

# Nombre de la sala donde hay que publicar las alarmas de tráfico
SPARK_ROOM_NAME = 'Milagro'


data = [
    {
        'nombre': 'ssh',
        'sent': 123,
        'rcv': 80,
        'from': 'adlfkjasldkf'
    }, {
        'nombre': 'dropbox',
        'sent': 123,
        'rcv': 80
    },
]


apps = []

for app in data:

    temp_dict = {
        'nombre': app['nombre'],
        'sent': app['sent'],
        'rcv': app['rcv'],
        'pirulo': 'alsdfjaklsdf'
    }

    apps.append(temp_dict)

