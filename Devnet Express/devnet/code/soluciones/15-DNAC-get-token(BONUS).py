"""
This script retrieves an authentication token from DNAC and prints out it's value
It is standalone, there is no dependency.
"""

import requests   # We use Python "requests" module to do HTTP GET query
# DNAC uses basic Authentication to get a token, but we are not using it
#from requests.auth import HTTPBasicAuth

# Import JSON encoder and decode module
import json
# Import base64 to encode username and password in an Authorization header
import base64

requests.packages.urllib3.disable_warnings()  # Disable warnings

# DNAC IP, modify these parameters if you are using your own DNAC
dnac_ip = "sandboxdnac.cisco.com"
username = "devnetuser"
password = "Cisco123!"
version = "v1"

# POST token API URL
post_url = "https://" + dnac_ip + "/api/system/" + version + "/auth/token"

# Encoding username:password in base64
encoded_user_pass = base64.b64encode(
    bytes(username + ':' + password, 'utf-8')).decode('utf-8')

# All DNAC REST API request and response content type is JSON.
# Adding Authorization header with the encoded username and password
headers = {
    'content-type': 'application/json',
    'Authorization': 'Basic ' + encoded_user_pass
}

# Make request and get response - "resp" is the response of this request
resp = requests.post(post_url, headers=headers, verify=False)
print ("Request Status: ", resp.status_code)

# Get the json-encoded content from response
response_json = resp.json()
print ("\nRaw response from POST token request:\n", resp.text)
# Not that easy to read the raw response, so try the formatted print out

# Pretty print the raw response
print ("\nPretty print response:\n", json.dumps(response_json, indent=4))
