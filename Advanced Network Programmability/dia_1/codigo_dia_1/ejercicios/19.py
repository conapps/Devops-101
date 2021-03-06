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
HEADERS = {
    'Content-Type': "application/yang-data+json",
    'Accept': "application/yang-data+json",
}

next_hop = # completar aqui
prefix = # completar aqui
mask = # completar aqui
interface = # completar aqui

body = {
    'Cisco-IOS-XE-native:native': {
        'ip': {
            'route': {
                'ip-route-interface-forwarding-list': [
                    {
                        "fwd-list": [
                            {
                                "interface-next-hop": [
                                    {
                                        "ip-address": next_hop
                                    }
                                ],
                                "fwd": interface
                            }
                        ],
                        "prefix": prefix,
                        "mask": mask
                    }
                ]
            }
        }
    }
}

def generic_patch(body, username=USERNAME, password=PASSWORD, **kwargs):
    url = BASE_DATA + kwargs['endpoint']
    response = requests.patch(url, headers=HEADERS, auth=HTTPBasicAuth(username, password), data=json.dumps(body), timeout=3, verify=False)
    if response.status_code in range(200, 300):
        print('Successful request, status code:', response.status_code)
    else:
        print('Error in the request, status code:', response.status_code)
        print(response.text)

if __name__ == "__main__":
    generic_patch(body, endpoint=ENDPOINT)