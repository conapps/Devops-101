import requests
import json
import urllib3
from requests.auth import HTTPBasicAuth

#disable warnings in requests from self signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Resolver el ejercicio aqui

if __name__ == '__main__':
    get_yang_modules(show=True)