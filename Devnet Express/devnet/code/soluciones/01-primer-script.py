"""
Script #1

Imprime texto en la consola con colores.
"""

# Este bloque es solo para poder importar del modulo 'helpers'
# que se encuentra en un directorio superior. No es necesario
# realizar esto desde la carpeta ~/code/.
# ****
import os
import sys
import inspect
DIR = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))
)
PARENT = os.path.dirname(DIR)
sys.path.insert(0, PARENT)
# ****

from helpers import curry

COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'blue': '\033[94m',
    'endc': '\033[0m'
}

def puts(text, color='green'):
    """ Prints to the console with colors if the color is defined. """
    if COLORS.get(color):
        print(COLORS[color] + text + COLORS['endc'] + '\n')
    else:
        print(text + '\n')

red = curry(puts, 'red')
blue = curry(puts, 'blue')

# Add a new line
print()

red("CONATEL S.A.")
puts("Devnet express.")
blue("Cisco .:|:.:|:.")
