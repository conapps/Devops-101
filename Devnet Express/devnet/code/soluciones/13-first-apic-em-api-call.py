"""
Script #13 - First APIC-EM API call.
"""

import json
import requests

# Disable warnings.
requests.packages.urllib3.disable_warnings()

URL = "https://devnetapi.cisco.com/sandbox/apic_em/api/v1"
# Ticket API endpoint.
API = "/ticket"

# APIC-EM espera que el JSON del request viaje en formato de texto.
PAYLOAD = json.dumps({
    "username": "devnetuser",
    "password": "Cisco123!"
})
# Definir los encabezados necesarios.
HEADERS = {
    "Content-Type": "application/json"
}

# Realizar el request pasando los parámetros correspondientes.
RESPONSE = requests.post(URL + API, data=PAYLOAD, headers=HEADERS, verify=False)
# Transformar la respuesta a JSON.
JSON = RESPONSE.json()

# Completar el print para incluir solo el valor del service ticket.
print("Authentication Token:", JSON["response"]["serviceTicket"])
