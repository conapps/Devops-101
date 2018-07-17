"""
Script #13 - First APIC-EM API call.
"""

import json
import requests

# Disable warnings.
requests.packages.urllib3.disable_warnings()

URL = "https://devnetapi.cisco.com/sandbox/apic_em/api/v1"
# 1. Endpoint del APIC-EM para obtener el service ticket.
API = None

# APIC-EM espera que el JSON del request viaje en formato de texto.
PAYLOAD = json.dumps({
    # Incluir las credenciales.
})
# Definir los encabezados necesarios.
HEADERS = {}

# Realizar el request pasando los parámetros correspondientes.
RESPONSE = None
# Transformar la respuesta a JSON.
JSON = None

# Completar el print para incluir solo el valor del service ticket.
print("Authentication Token:", None)
