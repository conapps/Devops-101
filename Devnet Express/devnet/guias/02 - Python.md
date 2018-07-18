# Python

## Python, interprete y versión

Es bastante sencillo chequear que versión de Python tenemos instalada en nuestro sistema. Por ejemplo, en Windows se accede a una terminal y se ejecuta el comando `python -V`. Si tienes múltiples versiones de Python instaladas, tal vez necesites escribir `py -3 -V` o `python3 -V`

```bash
$ python -V

$ py -3 -V

$ python3 -V
```

## Hola Mundo!

1.  Inicia el intérprete de Python con el comando apropiado para tu sistema. Por ejemplo, en Windows deberías escribir `python` o `py` y luego enter.
2.  Una vez dentro del intérprete escribe `>>> print("Hello world")`.
3.  Cuando hayas terminado, puedes salir del intérprete con cualquiera de los siguientes comandos `>>> exit()` o `>>> quit()`

## Scripts en Python

Un script en Python es simplemente un archivo de texto que tiene dos características escenciales:

1.  El script contiene código con la sintáxis de Python. Por ejemplo, podría escribir en un archivo de texto:
    `print("Soy un script de Python!")` y salvarlo. Técnicamente esto convertiría a dicho archivo en un script dado que `print` es una función nativa del lenguaje, y estamos utilizando la sintáxis adecuada para llamar a la función.
2.  El script tiene la extensión `.py`. Si bien esto no es estrictamente mandatorio, (se podría correr el script aunque tenga una extensión `.txt`), para que un archivo sea considerado verdaderamente un script de Python debe tener la extesión `.py`.

Correr un script de Python es bastante sencillo. Por ejemplo, en Windows, desde una terminal, se debe de escribir `py` o `python`, seguido del nombre del archivo y luego enter. Si no estamos ubicados en el mismo directorio donde se encuentra el script, entonces hay que indicar el camino completo seguido por el nombre del script.

```bash
$ python script.py
```

### Script #1

Vamos a escribir nuestro primer script de Python. El mismo contiene varios componentes que vamos a desarrollar sobre este curso. Por ahora, solo copiaremos el script que aparece a continuación y lo correremos.

**Recomendación:** Intente escribir el codigo en el editor de texto en lugar de copiarlo para empezar a acostumbrarse a escibir codigo.

#### Instrucciones

1.  Ir al archivo `code/01-primer-script.py`.
2.  Copiar o redactar el siguiente contenido dentro del archivo:

```python
""" 01 - Primer script """

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
print('\n')

red("CONATEL S.A.")
puts("Devnet express.")
blue("Cisco .:|:.:|:.")
```

## Python Basics

Si has escrito código en otros lenguajes, habrás notado que ciertas instrucciones definen su alcance a través de llaves.

El siguiente es un ejemplo utilizando el lenguaje de programación C. Es importante notar aquí que la sentencia `if` define su alcance utilizando las llaves `{}`

```c
#include <stdio.h>

printf("Hello World!");
num = 1;
if(num < 1){
    printf("This is C language and I'm less than 1!");
    printf("Goodbye Cruel World!");
}
```

Python no utiliza llaves para definir el alcance de sus sentencias, sino que en su lugar utiliza la indentación.
La indentación puede estar compuesta por espacio o tabulaciones, pero debe ser consistente en todo el código o el intérprete arrojará un error.

Considera el siguiente código Python:

```python
print ("Hola mundo!")
num = 1
if num < 1:
   print ("I'm less than 1!")
   print ("Goodbye Cruel World!")
```

Cuando se corre un script de Python, el intérprete comienza leyendo el código desde arriba hacia abajo. A medida que recorre cada instrucción, o bien la ejecuta, o la guarda en memoria para uso futuro.

1.  En la primer línea, el intérprete imprime a pantalla el texto `Hola mundo!` tal como lo indica la función invocada. Notese que la función `print` es nativa del lenguaje.
2.  En la segunda línea, se crea una variable llamada `num` y se le asigna el valor `1`. Por cierto, la variable podría haber tenido cualquier otro nombre desde `mi_variable` hasta `pepe`. Se puede profundizar sobre como nombrar variables en Python aquí:
    [PEP8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/?#naming-conventions)
3.  En la próxima línea el intérprete chequea el valor de la variable `num`, preguntando si la misma es menor a 1. El símbolo `<` es un operador. Python tiene varios tipos de operadores, entre los que se encuentran los operadores de comparación, asignación y aritméticos; discutiremos sobre operadores mas adelante. A la instrucción `if` se la llama condicional porque chequea una condición y ejecuta un bloque de código si y sólo si la misma es evaluada como `True`. A nivel de sintáxis, es importante notar que la instrucción `if` termina con dos putos `:`. En Python, muchas instrucciónes como los condicionales, funciones y bucles terminan con dos puntos.

4.  Es muy importante notar que las próximas dos instrucciones están indentadas. Esta indentación significa que estas instrucciones están dentro del bloque condicional. Dado que la condición es evaluada como `False` (debido a que la variable `num` vale 1 y 1 no es menor a 1), las instrucciones indentadas no son ejecutadas por el intpérprete.

### Script #2

Este segundo script muestra como funcionan las reglas de `scope` en Python. Podemos ver como se escriben expresiones condicionales, y como utilizamos operadores para evaluar el valor contenido dentro de nuestras variables.

#### Instrucciones

1.  Ir al archivo `code/02-segundo-script.py`.
2.  Copiar o redactar el siguiente contenido dentro del archivo:

```python
""" Segundo script """

print("Helloworld!")

NUM = 1

if NUM < 1:
    print("I'm less than 1!")
elif NUM == 1:
    print("I'm equal to 1.")
else:
    print("Goodbye Cruel World!")

print("I always get printed!")

VAL = 134

print("the value is: ", VAL)

print("the VAL is " + str(VAL))

NEW_VAL = "the VALue is" + str(VAL)
```

## Operadores

Si bien Python tiene muchos operadores, en este curso nos enfocaremos en los operadores más básicos. Los operadores de asignación y los de comparación.

Las tablas a continuación muestran un resumen de los operadores en Python y ejemplos básicos de su uso.

---

### Operadores aritméticos.

<table class="table table-bordered">
<tbody><tr>
<th style="width:10%">Operador</th>
<th style="width:45%">Descripción</th>
<th>Ejemplo</th>
</tr>
<tr>
<td>+ Addition</td>
<td>Adds values on either side of the operator.</td>
<td>a + b = 30</td>
</tr>
<tr>
<td>- Subtraction</td>
<td>Subtracts right hand operand from left hand operand.</td>
<td>a – b = -10</td>
</tr>
<tr>
<td>* Multiplication</td>
<td>Multiplies values on either side of the operator</td>
<td>a * b = 200</td>
</tr>
<tr>
<td>/ Division</td>
<td>Divides left hand operand by right hand operand</td>
<td>b / a = 2</td>
</tr>
<tr>
<td>% Modulus</td>
<td>Divides left hand operand by right hand operand and returns remainder</td>
<td>b % a = 0</td>
</tr>
<tr>
<td>** Exponent</td>
<td>Performs exponential (power) calculation on operators</td>
<td>a**b =10 to the power 20</td>
</tr>
<tr>
<td>//</td>
<td>Floor Division - The division of operands where the result is the quotient in which the digits after the decimal point are removed. But if one of the operands is negative, the result is floored, i.e., rounded away from zero (towards negative infinity):</td>
<td>9//2 = 4 and 9.0//2.0 = 4.0, -11//3 = -4, -11.0//3 = -4.0</td>
</tr>
</tbody></table>

### Operadores de comparación

<table class="table table-bordered">
<tbody><tr>
<th style="width:10%">Operador</th><th style="width:45%">Descripción</th><th>Ejemplo</th>
</tr>
<tr>
<td>==</td>
<td>If the values of two operands are equal, then the condition becomes true.</td>
<td> (a == b) is not true.</td>
</tr>
<tr>
<td>!=</td>
<td>If values of two operands are not equal, then condition becomes true.</td>
</tr>
<!--<tr>
<td>&lt;&gt;</td>
<td>If values of two operands are not equal, then condition becomes true.</td>
<td> (a &lt;&gt; b) is true. This is similar to != operator.</td>
</tr>-->
<tr>
<td>&gt;</td>
<td>If the value of left operand is greater than the value of right operand, then condition becomes true.</td>
<td> (a &gt; b) is not true.</td>
</tr>
<tr>
<td>&lt;</td>
<td>If the value of left operand is less than the value of right operand, then condition becomes true.</td>
<td> (a &lt; b) is true.</td>
</tr>
<tr>
<td>&gt;=</td>
<td>If the value of left operand is greater than or equal to the value of right operand, then condition becomes true.</td>
<td> (a &gt;= b) is not true. </td>
</tr>
<tr>
<td>&lt;=</td>
<td>If the value of left operand is less than or equal to the value of right operand, then condition becomes true.</td>
<td> (a &lt;= b) is true. </td>
</tr>
</tbody></table>

### Operadores de asignación

<table class="table table-bordered">
<tbody><tr>
<th style="width:10%">Operador</th>
<th style="width:45%">Descripción</th>
<th>Ejemplo</th>
</tr>
<tr>
<td>=</td>
<td>Assigns values from right side operands to left side operand</td>
<td>c = a + b assigns value of a + b into c</td>
</tr>
<tr>
<td>+=
Add AND</td>
<td>It adds right operand to the left operand and assign the result to left operand</td>
<td>c += a is equivalent to c = c + a</td>
</tr>
<tr>
<td>-=
Subtract AND</td>
<td>It subtracts right operand from the left operand and assign the result to left operand</td>
<td>c -= a is equivalent to c = c - a</td>
</tr>
<tr>
<td>*=
Multiply AND</td>
<td>It multiplies right operand with the left operand and assign the result to left operand</td>
<td>c *= a is equivalent to c = c * a</td>
</tr>
<tr>
<td>/=
Divide AND</td>
<td>It divides left operand with the right operand and assign the result to left operand</td>
<td>c /= a is equivalent to c = c / ac /= a is equivalent to c = c / a</td>
</tr>
<tr>
<td>%=
Modulus AND</td>
<td>It takes modulus using two operands and assign the result to left operand</td>
<td>c %= a is equivalent to c = c % a</td>
</tr>
<tr>
<td>**=
Exponent AND</td>
<td>Performs exponential (power) calculation on operators and assign value to the left operand</td>
<td>c **= a is equivalent to c = c ** a</td>
</tr>
<tr>
<td>//=
Floor Division</td>
<td>It performs floor division on operators and assign value to the left operand</td>
<td>c //= a is equivalent to c = c // a</td>
</tr>
</tbody></table>

### Operadores a nivel de bit

<table class="table table-bordered">
<tbody><tr>
<th style="width:10%">Operador</th>
<th style="width:45%">Descripción</th>
<th>Ejemplo</th>
</tr>
<tr>
<td>&amp; Binary AND</td>
<td>Operator copies a bit to the result if it exists in both operands </td>
<td> (a &amp; b) (means 0000 1100)</td>
</tr>
<tr>
<td>| Binary OR</td>
<td>It copies a bit if it exists in either operand.</td>
<td> (a | b) = 61 (means 0011 1101)</td>
</tr>
<tr>
<td>^ Binary XOR</td>
<td>It copies the bit if it is set in one operand but not both.</td>
<td> (a ^ b) = 49 (means 0011 0001)</td>
</tr>
<tr>
<td>~ Binary
Ones Complement</td>
<td>It is unary and has the effect of 'flipping' bits.</td>
<td> (~a ) = -61 (means 1100 0011 in 2's complement form due to a signed binary number.</td>
</tr>
<tr>
<td>&lt;&lt; Binary Left Shift</td>
<td>The left operands value is moved left by the number of bits specified by the right operand.</td>
<td> a &lt;&lt; = 240
(means 1111 0000)</td>
</tr>
<tr>
<td>&gt;&gt; Binary Right Shift</td>
<td>The left operands value is moved right by the number of bits specified by the right operand.</td>
<td> a &gt;&gt; = 15
(means 0000 1111)</td>
</tr>
</tbody></table>

### Operadores de membresía o pertenencia

<table class="table table-bordered">
<tbody><tr>
<th style="width:10%">Operator</th><th style="width:45%">Description</th><th>Example</th>
</tr>
<tr>
<td>in</td>
<td>Evaluates to true if it finds a variable in the specified sequence and false otherwise.</td>
<td>x in y, here in results in a 1 if x is a member of sequence y.</td>
</tr>
<tr>
<td>not in</td>
<td>Evaluates to true if it does not finds a variable in the specified sequence and false otherwise.</td>
<td>x not in y, here not in results in a 1 if x is not a member of sequence y.</td>
</tr>
</tbody></table>

### Operadores de identidad

<table class="table table-bordered">
<tbody><tr>
<th style="width:10%">Operador</th><th style="width:45%">Descripción</th><th>Ejemplo</th>
</tr>
<tr>
<td>is</td><td>Evaluates to true if the variables on either side of the operator point to the same object and false otherwise.</td><td> x is y, here <b>is</b> results in 1 if id(x) equals id(y).</td>
</tr>
<tr>
<td>is not</td><td>Evaluates to false if the variables on either side of the operator point to the same object and true otherwise.</td><td> x is not y, here <b>is not</b> results in 1 if id(x) is not equal to id(y).</td>
</tr>
</tbody></table>

### Precedencia de los operadores en Python

<table class="table table-bordered">
<tbody><tr><th>Operador</th><th>Descripción</th></tr>
<tr>
<td>**</td>
<td>Exponentiation (raise to the power)</td>
</tr><tr>
<td>~ + -</td>
<td>Complement, unary plus and minus (method names for the last two are +@ and -@)</td>
</tr><tr>
<td>* / % //</td>
<td>Multiply, divide, modulo and floor division</td>
</tr><tr>
<td>+ -</td>
<td>Addition and subtraction</td>
</tr>
<tr>
<td>&gt;&gt; &lt;&lt;</td>
<td>Right and left bitwise shift</td>
</tr><tr>
<td>&amp;</td>
<td>Bitwise 'AND'</td><td>
</td></tr><tr>
<td>^ |</td>
<td>Bitwise exclusive `OR' and regular `OR'</td>
</tr><tr>
<td>&lt;= &lt; &gt; &gt;=</td>
<td>Comparison operators</td>
</tr><tr>
<td>&lt;&gt; == !=</td>
<td>Equality operators</td>
</tr>
<tr>
<td>= %= /= //= -= += *= **=</td>
<td>Assignment operators</td>
</tr>
<tr>
<td>is is not</td>
<td>Identity operators</td>
</tr>
<tr>
<td>in not in</td>
<td>Membership operators</td>
</tr><tr>
<td>not or and</td>
<td>Logical operators</td>
</tr>
</tbody></table>

---

A modo de ejmplo, considera el código Python a continuación, (es el mismo que ya vimos anteriormente).
El bloque condicional `if num < 1:` utiliza el operador de comparación "menor-que" `<` que en este caso evalúa a `False` dado que 1 no es menor que 1.

```python
print ("Hello World!")
num = 1
if num < 1:
   print ("I'm less than 1!")
   print ("Goodbye Cruel World!")
```

## Condicionales

En el ejemplo anterior hemos discutido como el bloque condicional `if num < 1:` evalúa a `False` y por tanto saltea la ejecución de las instrucciones dentro de dicho bloque. Sin embargo, muchas veces un desarrollador está interesado en tomar alguna acción cuando la condición no se cumple.

Por ejemplo:

```python
print ("Hello World!")
num = 1
if num < 1:
  print ("I'm less than 1!")
  print ("Goodbye Cruel World!")
elif num == 1:
  print("I'm equal to 1!")
else:
  print("I'm greater than 1!")
```

En el código mas arriba hemos agregado una nueva condición para chequear y una acción por defecto para tomar si ninguna de las dos condiciones anteriores se cumplen (evalúan a `True`).

Si alguno de las condiciones se cumple, se ejecutará el bloque de código perteneciente a dicha condición y ningún otro.

Si ninguna de las condiciones se cumple, se ejecutará el bloque de código correspondiente a la condición por defecto `else:`. Vale la pena resaltar que este bloque de código asociado a la condición por defecto solo se ejecuta si ninguna de las condiciones se cumple.

Para terminar de entender el concepto, puedes correr el código mas arriba tres veces modificando el valor asignado a la variable `num` en cada corrida con los siguientes valores: 0, 1 y 2.

### Script #3

Para ver funcionar el condicional vamos a escribir un script que permita consumir valores al momento de ser llamados. Cuando llamemos este script vamos a pasar un número, el cual usaremos para realizar la evaluación y verificar el funcionamiento de un condicional.

#### Instrucciones

1.  Ir al archivo `code/03-tercer-script.py`.
2.  Copiar o redactar el siguiente contenido dentro del archivo:

```python
"""
Tercer script.
"""

import sys

NUM = int(sys.argv[1])

if NUM < 1:
    print("I'm less than 1!")
elif NUM > 1:
    print("I'm bigger than 1!")
else:
    print("I'm the default statement!")
```

## Defining Python Strings

Por varios motivos habrá veces en que necesitemos combinar texto y otros tipos de datos, así como asignarlos a variables y/o mostrarlos en pantalla.

Si bien hay muchas formas de concatenar strings
For purposes of readability and display there will be many times that the engineer will want to combine Python strings as well as other datatypes and assign them to variables and/or display on the screen. While there are several methods to combine strings in Python we're going to first focus on the simplest one which is to use the plus `+` operator to combine strings, otherwise known as concatenation. Let's look at a few examples below.

```python
myVarRed= "Red"
myVarBlue= "Blue"

print("Roses are Red. " + "Violets are Blue.")
print("Roses are " + myVarRed + ". Violets are " + myVarBlue)

myStr = "Roses are Red. " + "Violets are Blue."
varStr = "Roses are " + myVarRed + ". Violets are " + myVarBlue

print(myStr)
print(varStr)
```

Now let's concatenate different data types. Python expects concatenated data to be the string datatype, but in the example below we have strings and integers. As a result, we have to wrap each integer in a built-in Python function called `str()` that converts a simple datatype like an integer to a string.

```python
name = "Joe"
feet= 6
inches= 2

print("My name is " + name + ". I'm " + str(feet) + " feet " + str(inches) + " inches tall.")

myStr = "My name is " + name + ". I'm " + str(feet) + " feet " + str(inches) + " inches tall."
print(myStr)
```

### Combining Python Strings Using the , Operator

Using the `+` operator to combine Python strings is fairly intuitive, but as you've seen datatypes that are not strings need to be accounted for and converted into strings. Python provides another way to combine strings that does this conversion automatically when using the comma `,` operator if the operation is inside the print function. Let's review the first few lines of the last example using this new operator.

```python
name = "Joe"
feet= 6
inches= 2

print("My name is ",name,". I'm ",feet," feet ",inches," inches tall.")
```

Please note that this concatenation operation will not work as expected if you try to assign it to a variable, and then print it as the data is not concatenated.

```python
name = "Joe"
feet= 6
inches= 2

myStr="My name is ",name,". I'm ",feet," feet ",inches," inches tall."
print(myStr)
```

### Script #4 - `concat.py`

El siguiente script tiene las distintas maneras que vimos para concatenar strings. Una de ellas tiene un error, que hace que el script falle cuando lo corremos. La idea es encontrar donde esta el error.

#### Instrucciones

1.  Ir al archivo `code/04-concat.py`.
2.  Correr el script y verificar que existe un error con el mismo.
3.  Solucionar el error y verificar su funcionamiento corriendolo nuevamente.

## Python Data Types

In this step we'll explore Python data types. There are many data types listed in the figure below. There are simple numeric ones like **integers** and **floats**. For our purposes the differences between a float and an integer is that a float has a decimal in it. For example `52.856` is a float while `52` is an integer. `Boolean` data types can only be either `True` or `False`. Text is a data type that is shrouded in quotes `"text"` and can be alphanumeric. Text is more commonly called `string`. For example: `"brett"` is a `string`, so is `'brett123'`, but `123` is an `integer`.

![python data types](https://learninglabs.cisco.com/posts/files/00-prep-04-python-primer2/assets/images/python-datatypes.png)

There are also more complex data types such as lists, tuples and dictionaries. Let's explore these types.

### Lists

A list contains any number of sequential elements and is defined by square brackets `[]`. Here's a list:

```python
[
  'Martha',
  'Betty',
  5,
]
```

Which contains strings and an integer. Assigning a list to a variable is as simple as `var = ['Martha', 'Betty', 5]`. Lists are mutable which means that **they can be changed**. You can add data to a list, modify, delete it or even sort it. Notice that lists can have different data types inside them.

### Tuples

A tuple contains any number of sequential elements and is defined by parenthesis `()`. Here's a tuple `('Brett',9,'Cisco')`. Assigning a tuple to a variable is simple: `var1 = ('Brett',9,'Cisco')` which contains `strings` and an `integer`. Tuples are similar to lists, but they are immutable which means they **cannot be changed**. You might use a tuple to group similar data. For example, referring to the tuple defined above the similarity is that my name is Brett and I've worked at Cisco for 9 years. Because tuples are immutable they are more efficient meaning that their data can be accessed more quickly than lists.

While lists and tuples are defined a little differently, they both have their data accessed the same manner which is by square brackets `[]`. The first data element always starts at **position zero**. In the example in the list that was defined earlier, `var = ['Martha', 'Betty', 5]`, if I entered the python statement `print(var[0])`, it would display `Martha`. If I entered the python statement `print(var[1])`, it would display `Betty` and so on. The same syntax applies to tuples. For the tuple defined above, `var1 = ('Brett', 9, 'Cisco')`, if I entered the python statement `print(var1[0])`, it would display `Brett`. If I entered the python statement `print(var1[1])`, it would display 9 and so on.

### Dictionaries

A dictionary is a different than a list or a tuple. Each element in a dictionary must contain a key followed by a value. This key value association is typically referred to as name-value pairs. Dictionaries are defined by curly braces `{}`. Here's a dictionary:

```python
{
  "car": "corvette",
  "age": 7,
  "food": "pizza"
}
```

Assigning a dictionary to a variable is simple:

```python
myvar = {
  "car": "corvette",
  "age": 7,
  "food": "pizza"
}
```

The value in a dictionary is accessed by its key. For example if I entered the python statement `print(myvar["car"])`, it would display `corvette`. If I entered the python statement `print(myvar["food"])`, it would display pizza and so on. Dictionaries are sometimes also called `maps` or `associative arrays`.

![Python example data types](https://learninglabs.cisco.com/posts/files/00-prep-04-python-primer2/assets/images/python-datatypes2.png)

### Script #5 - `first-data-types.py`

En este script podemos ver las distintas formas de definir y acceder los distintos tipos de datos de python.

Al igual que en el script anterior, hay ciertos errores en el script que se tienen que resolver.

#### Instrucciones

1.  Ir al archivo `code/05-first-data-types.py`.
2.  Correr el script y verificar que existe un error con el mismo.
3.  Solucionar el error y verificar su funcionamiento corriendolo nuevamente.

## Defining and Accessing Nested Data Types

As discussed in Step 1, there are several complex data types which are lists, tuples and dictionaries. While each complex data type can exist on its own, there are many cases where one is nested inside the other. A common example is to have a dictionary of lists or the opposite such as a list of dictionaries.

For example, if I wanted to classify food by vegetables and desserts I'd create a list of vegetables and then a separate list of desserts. How can I organize these different lists into one complex datatype so I can access them? This question is a common one that software engineers ask and answer. In Python that nested datatype would look something like what's assigned to variables `food` below. Here we are using a dictionary datatype with the vegetables or desserts as the key followed by a list of each type. Recall that to access the value in the dictionary that we have to specify the key. And to access an element in a list that we need to specify the element number.

We might do a similar thing for cars, but here we'd like to list the make and model of each sports and classic car. In this case we use sports and classic as the keys and for the value we have a dictionary of the make and model of each car. Recall that to access the value in the dictionary that we have to specify the key, so in this case we specify the key twice - first to access the dictionary of sports car and second to access type sports car model.

```python
food = {
  "vegetables": [
    "carrots",
    "kale",
    "cucumber",
    "tomato"
  ],
  "desserts": [
    "cake",
    "ice cream",
    "donut"
  ]
}

print("My favorite vegetable is " + food["vegetables"][0])
print("My favorite dessert is " + food["desserts"][1])

cars = {
  "sports": {
    "Volkswagon": "Porsche",
    "Dodge": "Viper",
    "Chevy": "Corvette"
  },
  "classic": {
    "Mercedes-Benz": "300SL",
    "Toyota": "2000GT",
    "Lincoln": "Continental"
  }
}

print("My favorite sports car is a Dodge " + cars["sports"]["Dodge"])
print("My favorite classic car is a Lincoln " + cars["classic"]["Lincoln"])
```

### Script #6 - `nested-data-types.py`

Las listas, los diccionarios, y las tuplas, pueden crearese dentro de otros tipos, construyendo estructuras más complejas. Para acceder a los valores dentro de cada una de ellas, usamos la metodología explicada anteriormente.

Este script tiene configurado una estructura de datos compleja. La idea del ejercicio es imprimir en la consola:

1.  El segundo vegetal.
2.  El último postre.
3.  El modelo sport de Dodge.
4.  El modelo clasico de Lincoln.

#### Instrucciones

1.  Ir al archivo `code/06-nested-data-types.py`.
2.  Correr el script y verificar que los datos pedidos no son impresos.
3.  Modificar los comandos `print` para que sean impresos en la consola los valores requeridos.

## Python Loops

There are many reasons to write loops in Python or any coding language for that matter. The most common reason is that you have a list of data that you want to process. You might have noticed in the previous steps that when you wanted to access an object that you had to specify the element number or the key. Imagine how difficult that would be if you had to do the same thing for a hundred or a thousand objects! Loops make processing lists, tuples and dictionaries much easier because the loop will iterate through each object for you and you can then process the data via the source code that you write.

Let's start by looking at different types of loops in Python

The first type of loop uses the `range` function to specify a fixed amount of iterations that will occur in a loop. The first example specifies there should be `5` iterations. By default Python will start counting from `0` so going from `0` to `4` is `5` iterations. In the next example we provide a starting and ending point. Here there will be `3` iterations since python excludes the last number, so the iterations will be `2, 3, 4`. The `in` keyword is important because this keyword causes the value iterated over in the range to be assigned to the variable count. In this case that means that the variable name `count` is incremented with each iteration.

Similarly in the example `for fruit in basket`, **basket** is a list or dictionary that we iterate over and with each iteration the value found is assigned to the variable named `fruit` which we can then parse. In the final two examples, `while loops` don't assign a value to a variable and are typically used for processing inputs or data that is not in a list. For example, the `while True` infinite loop might be used when waiting for user input.

![Different python loops](https://learninglabs.cisco.com/posts/files/00-prep-04-python-primer2/assets/images/loops.png)

Using this new information about loops let's see how we can now process nested datatypes much more quickly. In step 2 you parsed the food and cars variables that contained nested data types. The solution required writing a line code to print each element. Observe the added code below under `#Parse datatypes with Loops` to see how much simpler and faster it is to access the data via looping.

```python
food = {
  "vegetables": [
    "carrots",
    "kale",
    "cucumber",
    "tomato"
  ],
  "desserts": [
    "cake",
    "ice cream",
    "donut"
  ]
}

print("My favorite vegetable is " + food["vegetables"][0])
print("My favorite vegetable is " + food["vegetables"][1])

cars = {
  "sports": {
    "Volkswagon": "Porsche",
    "Dodge": "Viper",
    "Chevy": "Corvette"
  },
  "classic": {
    "Mercedes-Benz": "300SL",
    "Toyota": "2000GT",
    "Lincoln": "Continental"
  }
}

print("My favorite sports car is a " + cars["sports"]["Dodge"])
print("My favorite sports car is a " + cars["sports"]["Chevy"])

#Parse datatypes with loops
for hungry in food["vegetables"]:
  print("My favorite vegetable is " + hungry)

for auto in cars["sports"]:
  print("My favorite sports car is a " + cars["sports"][auto])
```

### Script #7 - `nested-data-type-loops.py`

La idea es ver con este script algunos metodos básicos para iterar sobre una estructura de python, y así operar facilmentoe con los valores almacenados.

Dadas las estructuras de datos encontradas en el archivo `code/07-nested-data-type-loops.py`, escriba los `loops` necesarios para:

1.  Imprimir todos los vegetales.
2.  Imprimir todos los postres.
3.  Imprimir todos los modelos y marcas de autos sport.
4.  Imprimir todos los modelos y marcas de autos clasicos.

#### Instrucciones

1.  Ir al archivo `code/07-nested-data-type-loops.py`.
2.  Correr el script y verificar que los datos pedidos no son impresos.
3.  Agregar los loops necesarios para cumplir con lo pedido anteriormente.

## Python Functions

A function is a block of code that is run only when it's explicitly called. For example, print() is a built-in function written in Python that you've called many times. Functions are written to modularize code to make it easy to read, reuse and easier to debug because it's located in one place. Essentially, you don't want to write code over and over again that does the same thing. Instead you would put that code into a function and then call that function whenever you need it.

Let's look at the structure of a function, then we'll look at a simple example. In Python a function is defined in the manner shown below. The keyword def specifies that a function is defined which is then followed by the name of the function and optional arguments that are passed into it. Code to be included within the function must be indented under the function and become part of the function block. This code is then executed only when the function is called.

![Function structure](https://learninglabs.cisco.com/posts/files/00-prep-04-python-primer2/assets/images/function-struct.png)

Let's look at some simple examples of functions. The first function named `my_function` simply prints a statement. The second function `brett` takes an argument called val which it passes to the function `range` and uses for looping.

![Function examples](https://learninglabs.cisco.com/posts/files/00-prep-04-python-primer2/assets/images/function-ex.png)

Now let's look at these simple functions in a script to see how they're called. When a Python script is run the interpreter looks at what it should run now. The interpreter sees the call to print and executes that statement. It then sees the next two defined functions, makes note of them, but does not execute them because they have not yet been explicitly called. Continuing down the script the interpreter then sees the call to function `my_function` and executes it. Finally, it sees the call to function `brett` with the argument of 5 passed in and executes it.

```python
print("I'm not a function")

def my_function():
        print("Hey I'm a function!")

def brett(val):
    for i in range(val):
        print("I'm a function with args!")

my_function()
brett(5)
```

### Script #8 - `08-call-functions.py`

En este script hay varios ejemplos de funciones que imprimen en la consola. La idea es crear dos funciones nuevas que hagan lo mismo. La primera no debe tomar níngun argumento y debe escribir un texto fijo en la consola. La segunda, deberá tomar un argumento, e imprimirlo en la consola.

#### Instrucciones

1.  Ir al archivo `code/08-call-functions.py`.
2.  Correr el script y estudiar el error que tira.
3.  Crear las funciones correspondientes según los comentarios incluidos en el script.
4.  Probar que el script corre correctamente.
