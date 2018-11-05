from ncclient import manager


def print_capabilities(host, username, password, port='830', filter=''):
    # escribir codigo de la funcion aqui
    with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False) as router:
        for capability in router.server_capabilities:
            if filter in capability:
                print(capability)

if __name__ == "__main__":
    # para verificar el funcionamiento
    HOST = 'hostname'
    USERNAME = 'conatel'
    PASSWORD = 'conatel'
    filter = # Ingresar filtro aqui
    print_capabilities(HOST, USERNAME, PASSWORD, filter=filter)