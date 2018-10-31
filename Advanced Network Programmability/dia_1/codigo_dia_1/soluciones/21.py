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
ENDPOINT = 'Cisco-IOS-XE-native:native'
RESOURCE = '/ip'
HEADERS = {
    'Content-Type': "application/yang-data+json",
    'Accept': "application/yang-data+json",
}

next_hop_1 = '2.2.2.2'
prefix_1 = '1.1.1.1'
mask_1 = '255.255.255.255'
interface_1 = 'Null0'

next_hop_2 = '10.X.254.1' # sustituir 'X' por el numero de pod
prefix_2 = '0.0.0.0'
mask_2 = '0.0.0.0'
interface_2 = 'GigabitEthernet1'

rutas = [
    {
        "fwd-list": [
            {
                "interface-next-hop": [
                    {
                        "ip-address": next_hop_1
                    }
                ],
                "fwd": interface_1
            }
        ],
        "prefix": prefix_1,
        "mask": mask_1
    },
    {
        "fwd-list": [
            {
                "interface-next-hop": [
                    {
                        "ip-address": next_hop_2
                    }
                ],
                "fwd": interface_2
            }
        ],
        "prefix": prefix_2,
        "mask": mask_2
    }
]


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


def generic_put(body, username=USERNAME, password=PASSWORD, **kwargs):
    url = BASE_DATA + kwargs['endpoint'] + kwargs['resource']
    response = requests.put(url, headers=HEADERS, auth=HTTPBasicAuth(username, password), data=json.dumps(body), timeout=3, verify=False)
    if response.status_code in range(200, 300):
        print('Successful request, status code:', response.status_code)
    else:
        print('Error in the request, status code:', response.status_code)
        print(response.text)

if __name__ == "__main__":
    running = generic_get(endpoint=ENDPOINT)

    ip_body = {
        'Cisco-IOS-XE-native:ip': running['Cisco-IOS-XE-native:native']['ip']
    }

    ip_body['Cisco-IOS-XE-native:ip']['route']['ip-route-interface-forwarding-list'] = rutas

    generic_put(ip_body, endpoint=ENDPOINT, resource=RESOURCE)