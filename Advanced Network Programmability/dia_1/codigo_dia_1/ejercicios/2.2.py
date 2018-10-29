
# Disable certificate warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
import json


API_URL = 'https://t35nbzlj21.execute-api.us-east-1.amazonaws.com/produccion/users'

response = # hacer el request aquí

print(json.dumps(response.json(), indent=2))