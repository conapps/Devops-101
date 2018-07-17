"""
Script #11 - First python-spark api call
"""

import json
import requests

TOKEN = # Ingrese su clave de desarrollador de SPARK aqui.

def get_headers():
    """ Devuelve un diccionario con los encabezados necesarios. """
    return {
        "Authorization": "Bearer " + TOKEN,
        "Content-Type": "application/json; charset=utf-8"
    }
