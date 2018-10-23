import requests
import xmltodict

API = 'https://t35nbzlj21.execute-api.us-east-1.amazonaws.com/produccion'
ENDPOINT = '/mundiales-xml'

url = API + ENDPOINT

# Obtengo el Response object
respuesta = requests.get(url)

# Utilizo el atributo text del Response object para obtener la respuesta en unicode
respuesta_xml = respuesta.text

# respuesta_dict contiene ahora la respuesta en un diccionario
respuesta_dict = xmltodict.parse(respuesta_xml)

for mundial in respuesta_dict['mundiales']['mundial']:
    if mundial['campeon']['nombre'] == 'Brasil':
        # Imprimo información del mundial sólo si el campeón es Brasil
        print('Mundial', mundial['organizador'], mundial['fecha'])
        print('\tCampeón:', mundial['campeon']['nombre'])





