"""
This script retrieves an authentication token from DNAC and prints out it's value
It is standalone, there is no dependency.
"""

import requests   # We use Python "requests" module to do HTTP GET query
# DNAC uses basic Authentication to get a token
from requests.auth import HTTPBasicAuth
import json       # Import JSON encoder and decode module

requests.packages.urllib3.disable_warnings()  # Disable warnings

# Hardcoded URL data
dnac_ip = "sandboxdnac.cisco.com"
version = "v1"
api_root_system_url = "https://" + dnac_ip + "/api/system/" + version
api_root_url = "https://" + dnac_ip + "/api/" + version
api_endpoint = "/auth/token"
post_url = api_root_system_url + api_endpoint


def get_token(username, password, url=post_url):
    # All DNAC REST API request and response content type is JSON.
    headers = {'content-type': 'application/json'}


if __name__ == "__main__":
    print(get_token('devnetuser', 'Cisco123!'))
