import json
import requests

import urllib3
#disable warnings in requests from self signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from requests.auth import HTTPBasicAuth

# default values
HOST = 'https://hostname/'
USERNAME = 'conatel'
PASSWORD = 'conatel'

# Constants
BASE_DATA = HOST + 'restconf/data/'
HEADERS = {
    'Content-Type': "application/yang-data+json",
    'Accept': "application/yang-data+json",
}


def generic_get(username=USERNAME, password=PASSWORD, show=False, **kwargs):
    url = BASE_DATA + kwargs['endpoint'] + '?depth=unbounded'
    response = requests.get(url, headers=HEADERS, auth=HTTPBasicAuth(username, password), timeout=3, verify=False)
    if response.status_code in range(200, 300):
        print('Successful request, status code:', response.status_code)
        if show:
            print(json.dumps(response.json(), indent=2))
        return response.json()
    else:
        print('Error in the request, status code:', response.status_code)
        print(response.text)


if __name__ == '__main__':
    # invocar aquí la función