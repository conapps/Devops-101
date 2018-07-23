import requests
import sys
# Now we import our reusable components from solutions, just in case you don't have your own
from soluciones.DNAC import get_token, api_root_url

username = "devnetuser"
password = "Cisco123!"

api_endpoint = # Which endpoint do you need to user here?
url = api_root_url + api_endpoint

headers = {
    # Define headers here
    'content-type': 'application/json',
    'X-Auth-Token': # How do you get the token?
}

response = # Make the request here

i = 0
for device in # Place response iterable here:
    i += 1
    print('=== Equipo', i, ' ===')
    # More print statements below here
