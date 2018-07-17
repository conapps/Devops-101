import requests
import json

requests.packages.urllib3.disable_warnings()

URL = "https://api.ciscospark.com/v1"
ENDPOINT = "/people"

#Replace the {access-token} with your personal access token.
TOKEN = "Bearer NmY4ZTg2YjUtMzRmNy00Y2ZjLTkwOTYtNzYyODBlM2EyNTkzYjdiZDIwOTgtZTkz"

# Header information
HEADERS = {
  "content-type": "application/json; charset=utf-8",
  "authorization": TOKEN
}

# Parameter variable
PARAM = "?email=ialmandos@conatel.com.uy"

# Combine URL, API call and parameters variables
URL_COMPLETA = URL + ENDPOINT + PARAM

RESPONSE = requests.get(URL_COMPLETA, headers=HEADERS, verify=False)

response_json = json.loads(RESPONSE.text)

print(RESPONSE.text)
print(RESPONSE.json())
print(type(RESPONSE.json()))
