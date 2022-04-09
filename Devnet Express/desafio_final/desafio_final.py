import requests
import sys

# Constante que contiene el umbral de tráfico en Bytes
UMBRAL = int(sys.argv[1])
#UMBRAL = 1000000

# Constante que contiene el lapso de tiempo que hay que medir (un mes) medido en segundos
TIME_SPAN = 2592000

# Clave para poder autenticar con la API de Meraki
MERAKI_KEY = "definir el día del laboratorio"

# Nombre de la organización en Meraki que contiene la red para la cuál hay que obtener estadísticas
ORG_NAME = 'C008 - Preventa Conatel'

# Nombre de la red para cuál hay que obtener estadísticas
NETWORK_NAME = 'X001 - LAB CONATEL'

# Clave para poder autenticar con la API de Webex
WEBEX_KEY = 'definir el día del laboratorio'

# Nombre de la sala donde hay que publicar las alarmas de tráfico
WEBEX_ROOM_NAME = 'definir el día del laboratorio'

