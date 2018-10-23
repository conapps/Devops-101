import requests

API = 'https://t35nbzlj21.execute-api.us-east-1.amazonaws.com/produccion'
ENDPOINT = '/mundiales-xml'

url = API + ENDPOINT

# Obtengo el Response object
respuesta = requests.get(url)

# Utilizo el atributo text del Response object para obtener la respuesta en unicode
respuesta_xml = respuesta.text

print(respuesta_xml)




