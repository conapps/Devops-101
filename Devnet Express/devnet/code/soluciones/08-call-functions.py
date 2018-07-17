"""
Script #8 - Call functions.
"""

print("I'm not a function")

def my_function():
    """ This is a function """
    print("Hey I'm a function!")

def brett(range_max):
    """ Prints a range of 'range_max' size """
    for index in range(range_max):
        print(index)

def new_func(data):
    """ This is a new function """
    data2 = "my data is " + str(data)
    return data2

def print_multiply(num1, num2):
    """ Multiplies two numbers """
    print(num1 * num2)

my_function()

brett(5)

DATA = new_func("happy")

print(DATA)

print_multiply(5, 10)

# 1. Crear una función `my_func` que no tome nínguna variable y escriba en la
# consola.
def my_funct():
    """ Una función sin argumentos """
    print("Hola, soy una función sin argumentos.")

# 2. Crear una función `my_func2` que tome un argumento y lo escriba en la consola.
def my_funct2(argument):
    """ Una función con un argumento """
    print(str(argument))

my_funct()

my_funct2("Hola, soy una función con un argumento.")
