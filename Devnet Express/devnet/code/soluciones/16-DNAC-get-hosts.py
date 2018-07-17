"""
Script name: 14c-DNAC-get-hosts.py
Get all hosts connected to DNAC
"""
import requests
import json
import sys

# Now we import our reusable components from solutions, just in case you don't have your own
from DNAC import get_token, api_root_url

# Endpoint pointing to "hosts" resource
api_endpoint = "/host"
url = api_root_url + api_endpoint

headers = {
    # Define headers here
    'content-type': 'application/json',
    'X-Auth-Token': get_token('devnetuser', 'Cisco123!')
}

try:
    print('Making request to ', url)
    resp = requests.get(url, headers=headers, verify=False)
    response_json = resp.json()  # Get the json-encoded content from response
    # Convert "response_json" object to a JSON formatted string and print it out
    print (json.dumps(response_json, indent=4), '\n')
except:
    print ("Something wrong with GET /host request")
    sys.exit()

# Parsing raw response to list out all users and their role
for host in response_json["response"]:
    if 'connectedInterfaceName' in host:
        interface = host['connectedInterfaceName']
    else:
        interface = None

    print ("Host '%s': Connected to %s/%s" % (host['hostIp'],
                                              host["connectedNetworkDeviceName"],
                                              interface))
