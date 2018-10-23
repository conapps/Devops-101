import re
# Definirmos el texto como "string literal" para "escapar" los caracteres especiales
texto = """username conatel privilege 15 secret 5 $1$4Sf.$rjl0RjHG5\nODaninR1Myen0"""

exp = 'username\s([^ ]+)\s.*secret [0-9]\s([^\ ]+)'

username = re.search(exp, texto).group(1)
password =  re.search(exp, texto).group(2)

print('El usuario es:', username)
# repr() hace que los caracteres especiales como ser \n se impriman tal cual, sin interpretarse
print('El password es:', repr(password))

