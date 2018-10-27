import requests
from ncclient import manager

def pretty_print_xml(xml_string):
    """
    Funcion que recibe un string XML y lo imprime de forma bonita
    :param xml_string: string con formato XML
    :return: None
    """
    import xml.dom.minidom
    xml = xml.dom.minidom.parseString(xml_string)
    print(xml.toprettyxml())

def get_motd():
    URL = 'https://talaikis.com/api/quotes/random/'
    response = requests.get(URL, timeout=2).json()
    return response['quote']

def change_motd(host, username, password, message, port='830'):
    template = open('./config_motd.xml').read()
    # Completar la funcion

if __name__ == '__main__':
    # Agrego los caracteres delimitadores
    message = '^' + get_motd() + '^'
    print(message)
    change_motd('hostname', 'conatel', 'conatel', message)