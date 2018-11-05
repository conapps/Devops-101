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

next_hop_1 = '1.2.3.4'
prefix_1 = '10.10.10.10'
mask_1 = '255.255.255.255'
interface_1 = 'Null0'

next_hop_2 = '10.X.254.1' # sustituir 'X' por el numero de pod
prefix_2 = '0.0.0.0'
mask_2 = '0.0.0.0'
interface_2 = 'GigabitEthernet1'

body = {
    'Cisco-IOS-XE-native:ip': {
        'route': {
            'ip-route-interface-forwarding-list': [
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
        }
    }
}

# Definir generic_put aqui

if __name__ == "__main__":
    # llamar a generic_put aqui