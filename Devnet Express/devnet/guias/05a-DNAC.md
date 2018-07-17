# DNA Center

## Documentación de la API

[https://developer.cisco.com/site/dna-center-rest-api/](https://developer.cisco.com/site/dna-center-rest-api/)

## Introducción

El controlador DNA Center expone una API REST "Norte" que permite a los ingenieros y a las aplicaciones interactuar con el mismo de forma programática.

El controlador DNA Center también cuenta con interfaces "Sur" hacia el plano de control de la red; utiliza las mismas para gestionar e interactuar con los dispositivos de red.

De esta forma podemos utilizar la API Rest (Norte) para configurar el controlador y agregar funcionalidades de SDN a los equipos de red de forma dinámica.

## RBAC & service tokens

The Role-Based Access Control (RBAC) mechanism on the Cisco DNAC assigns a security role to every user account. That role determines which Cisco DNAC resources and operations are available for that user account.

The Cisco DNAC controller defines the following roles and privileges:

* **Administrator (SUPER_ADMIN-ROLE)** provides the user with full administrative privileges to all Cisco DNAC resources, including the ability to add or remove users and accounts.
* **Network Administrator (NETWORK_ADMIN-ROLE)** enables the user to provision, upgrade and change the configuration of network devices.
* **Observer (OBSERVER-ROLE)** provides the user with primarily read-only privileges to the Cisco DNAC.
* **Telemetry (TELEMETRY-ADMIN-ROLE)** enables the user to administer the telemetry (Assurance) configuration.

A security token known as a service token encapsulates user identity and role information as a single value.

RBAC-governed APIs use the service token to make access-control decisions. Therefore, to start, you send the Cisco DNAC a POST /token request with your username and password. If the DNAC controller authenticates your request, it returns a service token that encapsulates the role associated with the authenticated user account.

After you get the service token, you include it in all of the subsequent calls you send to the controller. When the controller receives those calls, it checks the service token before performing the action requested by the call.

## Generate a service token (script 14a)

Carefully review the [API documentation](https://developer.cisco.com/site/dna-center-rest-api/) regarding how to get a service token.
The procedure explained in the docs, assumes the use of a web browser (cookie based JWT).
In our case we are not using a browser to interact with the API; we are going to interact with it through a Python script.
Although both procedures are almost the same, they have some minor differences:

Procedure to get a token using POSTMAN:

1.  Configure the method as "POST"
2.  Configure the URL as: https://sandboxdnac.cisco.com/api/system/v1/auth/token
3.  Add a header `{"Content-Type":"application/json"}`
4.  Add a header `{"Authorization":"Basic <username:password>"}`
    Pay attention to the space after "Basic". <username:password> must be "devnetuser:Cisco123!" 
    encoded in Base64 (ZGV2bmV0dXNlcjpDaXNjbzEyMyE=)
5.  Submit and see the results in the body of the response.

Now let's see how to get a service token programmatically using Python:

1.  Locate the 15-DNAC-get-token.py.
2.  Use a Python command to run the script. For example:
    * On Linux or Mac OS: ```python3 15-DNAC-get-token.py```
    * On Windows: ```py -3 15-DNAC-get-token.py or python 14a-DNAC-get-token.py```
3.  Copy the service token printed in the console, navigate to [https://jwt.io](https://jwt.io), paste it inside "Encoded" text area and see the results in "Decoded" field.

> Observe that the function `HTTPBasicAuth` takes care of base64 encoding of the username and password and to include the encoded field in a header in the request.

**Bonus:**

> Read **Authentication/Authorization** section of the [API documentation](https://developer.cisco.com/site/dna-center-rest-api/), `import base64` and use the function `base64.b64encode(bytes(username + ':' + password, 'utf-8')).decode('utf-8')` to encode username:password in base64 and get the token **without** using `HTTPBasicAuth`.

## Prepare to reuse the generation of service tokens (script DNAC.py)

Now we are going to make a **python module** called `DNAC.py` with a function in it called `get_token(username, password)` that returns the service token as a string. Complete the script `DNAC.py` and obtain a re-usable function.

## Using the service token (Script 16)

Almost every API call you send to Cisco DNAC REST must provide a service token; it doesn't matter whether the request is a POST, GET, PUT or DELETE. To provide the service token with your call, use an X-Auth-Token header. The header is a name-value pair that includes the value of your service token:

`{"X-Auth-Token": "service_token_value" }`

Replace service_token_value with the value of your service token. You don't have to get a new service token every time you make a request. However, the service token value must be valid and unexpired. In this lab, for simplicity, you start by getting a new service token each time you make a call to the API. 

The following GET /host request shows how to use a service token. This request returns a list of DNAC hosts. The content of the list it returns is governed by the role of the caller. If the caller has an admin role, the response contains a list of all hosts. If the caller has an observer role, the response contains only the caller's host information.

The GET /host request does not require any arguments. Add an X-Auth-Token header to your GET /host request. The value of X-Auth-Token is the service token that your previous call to POST /token returned.

### Script 16.

Start from the file `16-DNAC-get-hosts.py` and modify it so it returns a list of hosts from DNAC.

## Network device related APIs

#### Objectives

The Cisco DNAC controller assigns a unique ID to every network device. You can pass this ID to a variety of network device-related calls to retrieve information about a specific device, such as its IOS configuration and interfaces.

In this lab, the Python application makes the following calls:

- `GET /network-device`
- `GET /network-device/{networkDeviceId}/config`
- `GET /interface/network-device/{deviceId}`

Note: The Cisco DNAC controller can scan for and discover physical devices attached to a network. To initiate this discovery process, you can send a POST /discovery call to the controller, or you can click the Discovery icon in its GUI. The Cisco DNAC controller in the Cisco DevNet Learning Labs is pre-populated with the results of a previous discovery, so this lab does not examine Discovery.

### Application that displays IOS configuration

In this section, you create a simple application to:

Prompt the user to select a device.
Display the IOS configuration of the user-selected device.
Pseudo-code:

1. Use GET /network-device to display a list of network devices with IP addresses.
2. Accept user input of device selection.
3. Use `GET /network-device/{deviceId}/config` to retrieve the IOS configuration of the specified device, then display the IOS configuration to the user.

### Task 1: Present a list of network devices with IP addresses (script 17)

To display a list of network devices to the user, retrieve network device information by issuing the `GET /network-device` request. The response body returns a list of network devices. Each block in the response provides information about a single device, including its network device name, IP, type, network device ID and more.

This **network device ID** provides a way of identifying a specific network device to many APIs, including the `GET /network-device/{deviceId}/config` request.

The `GET /network-device` response block provides many attributes. Your application uses the following attributes:

- **instanceUuid** or **id** is the ID the controller assigned to the network device at discovery.
- **hostname** is the name of the network device. Note that this attribute applies to both hosts and devices.
- **managementIpAddress** is the IP address of the network device.
- **type** is the type of network device, such as a switch, router, or access point.

Your task is the following: 

1. Locate and open the file `17-DNAC-get-network-device-list.py`
2. Modify it so the script executes a `GET /network-device` request and displays a list of devices in exactly the following format:

```
=== Equipo 1  ===
	Hostname:  asr1001-x.abc.inc
	Type:  Cisco ASR 1001-X Router
	Device id:  d5bbb4a9-a14d-4347-9546-89286e9f30d4
	Management IP Address:  10.10.22.74
=== Equipo 2  ===
	Hostname:  cat_9k_1.abc.inc
	Type:  Cisco Catalyst 9300 Switch
	Device id:  6d3eaa5d-bb39-4cc4-8881-4a2b2668d2dc
	Management IP Address:  10.10.22.66
=== Equipo 3  ===
	Hostname:  cat_9k_2.abc.inc
	Type:  Cisco Catalyst 9300 Switch
	Device id:  74b69532-5dc3-45a1-a0dd-6d1d10051f27
	Management IP Address:  10.10.22.70
=== Equipo 4  ===
	Hostname:  cs3850.abc.inc
	Type:  Cisco Catalyst38xx stack-able ethernet switch
	Device id:  8be78ab1-d684-49c1-8529-2b08e9c5a6d4
	Management IP Address:  10.10.22.69

```

### Task 2: Prompt the user for input and retrieve the device ID (script 17)

Add the following code to `17-DNAC-get-network-device-list.py` so it prompts the user for a device selection:

```python
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
```

### Task 3: Get the IOS configuration of the specified device and display it to the user (script 18)

Now, use the script `18-DNAC-get-network-config.py` (it starts where `17-DNAC-get-network-device-list.py` left) and complete it so it retreives the selected device configuration.
> Hint: You can ask DNA Center for a device configuration issuing a `GET /network-device/{device-id}/config`.