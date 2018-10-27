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

def generic_conf(host, username, password, port='830', **kwargs):
    template = open(kwargs['template']).read()
    config = template.format(**kwargs)
    with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False) as router:
        netconf_reply = router.edit_config(config, target='running')
        pretty_print_xml(netconf_reply.xml)

if __name__ == '__main__':

    params = {
        'description': 'test description from Netconf',
        'template': './interface_description.xml'
    }

    # Llamar a generic conf