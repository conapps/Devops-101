import requests
import json

# Disable warnings
requests.packages.urllib3.disable_warnings()

token = "Bearer NmY4ZTg2YjUtMzRmNy00Y2ZjLTkwOTYtNzYyODBlM2EyNTkzYjdiZDIwOTgtZTkz"

url = "https://api.ciscospark.com/v1"
endpoint = "/people"

headers = {
    'Authorization': token,
    'Content-Type': "application/json",
}

email = "ialmandos@conatel.com.uy"
param = "?email=" + email

# Now constructing the final url
url += endpoint + param

response = requests.get(url, headers=headers, verify=False).json()

for item in response["items"]:
    print('Nombre:', item['displayName'])
    print('Correo:', item['emails'][0])
