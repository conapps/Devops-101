import xmltodict
from ncclient import manager

def get_schema(schema, host, username, password, port='830'):
    with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False) as router:
        netconf_reply = router.get_schema(schema)
        print(xmltodict.parse(netconf_reply.xml)['rpc-reply']['data']['#text'])


if __name__ == "__main__":
    # para probar el script
    HOST = # hostname
    USERNAME = 'conatel'
    PASSWORD = 'conatel'
    get_schema('ietf-interfaces', HOST, USERNAME, PASSWORD)