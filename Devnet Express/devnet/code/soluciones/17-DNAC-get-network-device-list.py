import requests, sys
# Now we import our reusable components from solutions, just in case you don't have your own
from DNAC import get_token, api_root_url

username = "devnetuser"
password = "Cisco123!"

api_endpoint = "/network-device"
url = api_root_url + api_endpoint

headers = {
    # Define headers here
    'content-type': 'application/json',
    'X-Auth-Token': get_token('devnetuser', 'Cisco123!')
}

response = requests.get(url, headers=headers, verify=False).json()
i = 0
for device in response['response']:
    i += 1
    print('=== Equipo', i, ' ===')
    print('\tHostname: ', device['hostname'])
    print('\tType: ', device['type'])
    print('\tDevice id: ', device['id'])
    print('\tManagement IP Address: ', device['managementIpAddress'])

device_list = response['response']

while True:
    user_input = input('=> Selecciona uno de los siguientes equipos: ')
    # ignore space
    user_input = user_input.replace(" ", "")
    if user_input.lower() == 'exit':
        sys.exit()
    if user_input.isdigit():
        if int(user_input) in range(1, len(device_list) + 1):
            device_id = device_list[int(user_input)-1]['id']
            break
        else:
            print("Uups! el numero esta fuera de rango. Intenta de nuevo o escribe 'exit'\n")
    else:
        print("Uups debes seleccionar un numero o escribir 'exit'\n")

# End of while loop
print('El equipo seleccionado es el: ', device_id)