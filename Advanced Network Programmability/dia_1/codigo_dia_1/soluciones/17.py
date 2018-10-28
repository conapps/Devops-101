import requests
import json
import urllib3
from requests.auth import HTTPBasicAuth

#disable warnings in requests from self signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# default values
HOST = 'https://hostname/'
USERNAME = 'conatel'
PASSWORD = 'conatel'

# Constants
BASE_DATA = HOST + 'restconf/data/'
ENDPOINT_YANG_MODULES = 'ietf-yang-library:modules-state'
HEADERS = {
    'Content-Type': "application/yang-data+json",
    'Accept': "application/yang-data+json",
}


def get_yang_modules(username=USERNAME, password=PASSWORD, show=False):
    url = BASE_DATA + ENDPOINT_YANG_MODULES
    response = requests.get(url, headers=HEADERS, auth=HTTPBasicAuth(username, password), verify=False, timeout=3)

    if response.status_code in range(200, 300):
        print('Successful request, status code:', response.status_code)
        if show:
            print(json.dumps(response.json(), indent=2))
        return response.json()
    else:
        print('Error in the request, status code:', response.status_code)

def get_yang_definition(filter, show=False):
    modules = get_yang_modules()['ietf-yang-library:modules-state']['module']
    result = []

    for module in modules:
        if filter in module['name']:
            result.append(module)
    if show:
        for definition in result:
            print(json.dumps(definition, indent=2))
    return result

if __name__ == '__main__':
    get_yang_definition('Cisco-IOS-XE-native', show=True)