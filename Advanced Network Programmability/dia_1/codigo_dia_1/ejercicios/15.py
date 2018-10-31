from ncclient import manager

USERNAME = 'conatel'
PASSWORD = 'conatel'
HOSTNAME = # escribir hostname aqui


def pretty_print_xml(xml_string):
    """
    Funcion que recibe un string XML y lo imprime de forma bonita
    :param xml_string: string con formato XML
    :return: None
    """
    import xml.dom.minidom
    xml = xml.dom.minidom.parseString(xml_string)
    print(xml.toprettyxml())

def save_config(host, username, password, port='830'):
    from ncclient.xml_ import to_ele
    RPC = open('./save_config.xml', 'r').read()
    with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False) as router:
        netconf_reply = router.dispatch(to_ele(RPC))
        pretty_print_xml(netconf_reply.xml)

if __name__ == '__main__':
    # Llamar a save_config, no olvidar el armar previamente el filtro save_config.xml