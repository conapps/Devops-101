"""
Script #15 - Comunicación con la API de Meraki
"""

# Este bloque es solo para poder importar del modulo 'helpers'
# que se encuentra en un directorio superior. No es necesario
# realizar esto desde la carpeta ~/code/.
# ------------------------------------------------------------
import os
import sys
import inspect
DIR = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))
)
PARENT = os.path.dirname(DIR)
sys.path.insert(0, PARENT)
# ------------------------------------------------------------
import meraki
