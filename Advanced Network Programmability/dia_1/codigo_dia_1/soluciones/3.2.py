import requests

API = 'https://t35nbzlj21.execute-api.us-east-1.amazonaws.com/produccion'
ENDPOINT = '/mundiales'

url = API + ENDPOINT

# Obtengo el Response object
respuesta = requests.get(url)

# Utilizo el metodo json() del response object para obtener un diccionario
respuesta_dict = respuesta.json()


for mundial in respuesta_dict['mundiales']:
    if mundial['campeon']['copas'] > 1:
        print('Mundial', mundial['fecha'])
        print('\tOrganizador:', mundial['organizador'])
        print('\tCampeon:', mundial['campeon']['nombre'])
        print('\tCopas totales de', mundial['campeon']['nombre'] + ':', mundial['campeon']['copas'])
