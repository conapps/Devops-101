# JSON

## JSON - Conceptos básicos

**Java Script Object Notation** (JSON) es una estructura de datos en formato nombre-valor, diseñada para facilitar el intercambio de información entre aplicaciones. Fue pensado para ser muy liviano y fácilmente legible por un ser humano. Su diseño minimalista evita el exceso de texto que históricamente se le atribuyó a XML.

## La estructura JSON

En JSON, los datos se almacenan en pares nombre-valor, tal como si fuera un diccionario de Python. Sin embargo, en JSON nos referiremos a ellos como objetos en lugar de diccionarios.

Por ejemplo, `{"auto": "volvo", "fruta": "manzana"}` es un objeto JSON, pero luce exactamente igual a un diccionario de Python. Las diferencias entre JSON y las estructuras de datos de Python son mínimas; por ejemplo los booleanos se representan ligeramente distintos, `true` en JSON y `True` en Python.

En líneas generales, los datos se transmiten entre las APIs REST y los scripts de Python en formato JSON, mientras que se procesan dentro de los scripts utilizando las estructuras clásicas de datos de Python que hemos visto hasta ahora.
Para simplificar, desde el punto de vista de Python, una estructura de datos en JSON podría pensarse como una estructura de datos de Python, (un diccionario de listas por ejemplo), convertido a `String` con algunas modificaciones mínimas.

Para realizar este proceso de conversión, Python dispone de una librería: `json`. Esta librería cuenta con dos funciones principales `json.loads(datos_en_json)`, que toma datos en JSON y los convierte a diccionarios de Python, y `json.dumps(datos_en_python)` que toma estructuras de datos de Python y los convierte a JSON.

Una vez que convertimos los datos en JSON a estructuras de datos de Python, podemos utilizar todo lo que hemos aprendido hasta ahora para trabajar con dichas estructuras (diccionarios, tuplas, listas, bool, etc). En el siguiente ejemplo, supongamos que la variable `json_recibido_desde_api` contiene datos obtenidos a través de una consulta a una API REST y veamos como una vez que transformamos los datos en JSON a estructuras de datos de Python podemos procesarlos normalmente:

```python
json_recibido_desde_api = '{"auto": "volvo", "frutas": ["manzanas", "peras", "naranjas"]}'
mi_variable = json.loads(json_recibido_desde_api)

# Vamos a imprimir cada una de las frutas
for fruta in mi_variable["frutas"]:
  print(fruta)
```

En el trabajo diario con scripts de Python, típicamente interactuamos con APIs REST para obtener datos en formato JSON, luego convertimos estos datos a estructuras anidadas de Python (diccionarios de listas, listas de diccionarios, diccionarios de listas de diccionarios, etc), las procesamos y finalmente tomamos alguna acción.

Dado que repetiremos este proceso una y otra vez a lo largo del curso, a partir de ahora practicaremos mas en profundidad como recorrer estructuras anidadas en Python.

### Script #9 - `09-json-print.py`

#### Instrucciones

1.  Ir al archivo `code/09-json-print.py`.
2.  Seguir las instrucciones dentro del archivo.

## Estructuras JSON anidadas

Los objetos y arrays JSON que recibimos desde las APIs típicamente se encuentran anidados en varios niveles con el fin de organizar los datos. Por esto, una vez convertidos los datos JSON a estructuras de datos de Python nos encontraremos con estructuras como la del ejemplo. Allí podemos ver que tenemos un diccionario con una única llave, que contiene otro diccionario que a su vez contiene también una única llave y que el valor correspondiente a dicha llave es una lista de 4 elementos.

```python
myvar = {
  "donut": {
    "flavors": [
      "chocolate",
      "jelley",
      "maple",
      "plain"
    ]
  }
}

print(myvar["donut"]["flavors"][0])
>>> chocolate


print("My favorite donut flavors are:", end=" ")
for f in myvar["donut"]["flavors"]:
  print(f, end=" ")

>>> My favorite donut flavors are: chocolate jelley maple plain
```

Avancemos ahora con un ejemplo un poco mas complejo.
Intenta seguir seguir el ejemplo buscando las estructuras anidadas, recuerda: los diccionarios comienzan con `{` y las listas con `[`.

```python
myvar1 = {
  "type": "donut",
  "flavors": {
    "flavor": [{
      "type": "chocolate",
      "id": 1001
    }, {
      "type": "glazed",
      "id": 1002
    }, {
      "type": "sprinkled",
      "id": 1003
    }]
  }
}

print("Id: " + str(myvar1["flavors"]["flavor"][0]["id"]) + " type: " + myvar1["flavors"]["flavor"][0]["type"])
>>> Id: 1001 type: chocolate

for f in myvar1["flavors"]["flavor"]:
    print("Id is: " + str(f["id"]) + " type is: " + f["type"])

>>> Id is: 1001 type is: chocolate
>>> Id is: 1002 type is: glazed
>>> Id is: 1003 type is: sprinkled
```

### Script #10 - `10-json-nested-print.py`

El script contiene multiples ejemplos de como imprimir los valores dentro de estructuras de datos de python. La idea es, utilizando estos ejemplos como referencia, imprimir algunas estructuras de datos anidadas de complejidad media.

#### Instrucciones

1.  Ir al archivo `code/10-json-nested-print.py`.
2.  Imprimir las estructuras de datos de acuerdo a las instrucciones dentro del archivo.
