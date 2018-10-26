import json
import xmltodict

from ncclient import manager

# default constants
HOST = # hostname
PORT = '830'
USERNAME = 'conatel'
PASSWORD = 'conatel'

def pretty_print_xml(xml_string):
    """
    Funcion que recibe un string XML y lo imprime de forma bonita
    :param xml_string: string con formato XML
    :return: None
    """
    import xml.dom.minidom
    xml = xml.dom.minidom.parseString(xml_string)
    print(xml.toprettyxml())

def print_interfaces(host, username, password, port='830'):

    # loading filter
    filter = open('path to interfaces.xml').read()

    with manager.connect(host=host, username=username, password=password, port=port, hostkey_verify=False) as router:
        result = router.get(filter)
        interfaces = # obtener una lista de interfaces a partir de result
        # imporimir los nombres de las interfaces

if __name__ == "__main__":
    print_interfaces(host=HOST, username=USERNAME, password=PASSWORD)