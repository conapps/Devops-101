import requests
import sys

# Constante que contiene el umbral de tráfico en Bytes
UMBRAL = int(sys.argv[1])
#UMBRAL = 1000000

# Constante que contiene el lapso de tiempo que hay que medir (un mes) medido en segundos
TIME_SPAN = 2592000

# Clave para poder autenticar con la API de Meraki
MERAKI_KEY = "c3c60821f6c5e1c7928f76fd5b1e1305184a24f5"

# Nombre de la organización en Meraki que contiene la red para la cuál hay que obtener estadísticas
ORG_NAME = 'C008 - Preventa Conatel'

# Nombre de la red para cuál hay que obtener estadísticas
NETWORK_NAME = 'X001 - LAB CONATEL'

# Clave para poder autenticar con la API de Spark
SPARK_KEY = 'MDE5NmViZWItMzc4ZS00YzEwLTlhNzUtYjQ0NDQ2ZDlhMmRlNDFlNDhkY2MtNDQ5'

# Nombre de la sala donde hay que publicar las alarmas de tráfico
SPARK_ROOM_NAME = 'CONATEL - Devnet Express 2018'

