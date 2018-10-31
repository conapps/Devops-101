#!/usr/bin/python

# Disable certificate warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
import re
import json

SPARK_BASE_API = 'https://api.ciscospark.com/v1/'

def get_usernames():

    """
    Devuelve una lista con los usuarios configurados en el dispositivo
    :return: list of usernames
    """
    from cli import execute
    exp = re.compile(r'username\s([^\ ]+)\s.*secret [0-9]\s[^\ ]+?')
    show_command = execute("show running-config")
    while True:
        # Block intended to solve bug in cli module
        try:
            exp.search(show_command).group(0)
            break
        except:
            print('Ups show_command vacio, intentando de nuevo...')
            show_command = execute("show running-config")
    usuarios = exp.findall(show_command)
    if 'ec2-user' in usuarios:
        usuarios.remove('ec2-user')
    if 'conatel' in usuarios:
        usuarios.remove('conatel')
    return usuarios

def delete_usernames(usuarios):

    from cli import configure

    for usuario in usuarios:
        comando = "no username " + usuario
        print('Borrando usuario', usuario)
        try:
            configure(comando)
            print('Usuario', usuario, 'borrado')
        except Exception as error:
            raise ValueError('Error al borrar usuario: ' + str(error))

def delete_users():
    delete_usernames(get_usernames())

def get_hostname():
    from cli import execute
    command = 'show version'
    show_version = execute(command)
    exp = re.compile(r'([\w\d]+)\suptime is\s')
    hostname = exp.findall(show_version)
    return hostname[0]

def send_message(message, key):

    """
    Function that sends a message to Spark Team room using users ID
    :param message: String
    :param key: String
    :return: None
    """

    HEADERS = {
        'Authorization': 'Bearer ' + key,
        'Content-Type': 'application/json'
    }
    ROOM_ID = 'Y2lzY29zcGFyazovL3VzL1JPT00vZjE2MTZmNTAtOWZiZC0xMWU4LWFhNzEtZTlkMjFkNTdiOGFh'
    BODY = {
        'roomId': ROOM_ID,
        'text': message
    }
    URL = SPARK_BASE_API + 'messages'
    response = requests.post(URL, data=json.dumps(BODY), headers=HEADERS, timeout=2, verify=False)
    if response.status_code not in range(200, 301):
        raise RuntimeError('Error al enviar mensaje. Respuesta del Servidor Teams:', str(response.text))
