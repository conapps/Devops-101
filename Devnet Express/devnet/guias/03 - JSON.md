JSON
===

JSON Basics
---

JSON which stands for **Java Script Object Notation** consists of text-based name-value pairs making it simple for applications to store and exchange data. It's designed to be lightweight and readable as well as minimal so there's not excessive text which has sometimes been the complaint of XML which is another text-based protocol for exchanging and storing data.

The JSON Structure
---

In JSON data is set up in name value pairs just like a Python dictionary. However, in JSON dictionaries are referred to as objects. For example, `{"car": "volvo", "fruit": "apple"}` is a JSON object, but looks just like a Python dictionary. The object is assigned to a variable in the same manner as well: `var = {"car": "volvo", "fruit": "apple"}`. In addition, JSON data is accessed the same way as when accessing data in a Python dictionary. For example, to get the value for fruit in Python we would enter `var["fruit"]` which would return apple. To display this value we enter `print(var["fruit"])` . We can also loop through and display all of the keys and values.

```python
var = {
  "car": "volvo", 
  "fruit":"apple"
}
print(var["fruit"])
for f in var:
  print("key: " + f + " value: " + var[f])
```

As with Python, JSON also uses lists which it refers to as arrays. In JSON an array is typically nested in an object. For example, `{"donut": ["chocolate", "glazed", "sprinkled"]}` . Let's assign this JSON object to a variable: `var1 = {"donut": ["chocolate", "glazed", "sprinkled"]}`. Notice here that donut is the key, and the value is the array of the donut flavors. If I wanted to get the chocolate donut, I would access it by entering `var1["donut"][0]` which would return chocolate because it is the first element in the array. I could display the text by entering `print(var1["donut"][0])`. We'll loop through and display the values too.

### Script #9 - `09-json-print.py`

El documento contiene multiples ejemplos de como imprimir los valores dentro de documentos de python. La idea es utilizando estos ejemplos, imprimir todos los valores de los últimos dos elementos de JSON.

#### Instrucciones

1. Ir al archivo `code/09-json-print.py`.
2. Correr el script y estudiar el resultado.
3. Escribir el codigo necesario para imprimir todo el documento JSON y cada uno de sus valores individualmente.
4. Probar que el script corre correctamente.

Deeply Nested JSON Structures
---

In JSON objects and arrays are often nested several layers in order to organize data. In the following relatively simple example we classify the flavors of a `donut` and put them in an array as shown in JSON structure `{"donut": {"flavors": ["chocolate", "jelley", "maple", "plain"]}}`. Looking at this structure from the inside and moving outward you see that we've nested an array inside an object which itself is nested inside an object. With this structure starting from the outside and moving in we see that donut is the key with the object flavors being its value. But notice that flavors is also a key and its value is the array of donut flavors. As a result, to get the chocolate flavor we need to dig a little deeper. First we assign the JSON to a variable `myvar = {"donut": {"flavors": ["chocolate", "jelley", "maple", "plain"]}}` . We access chocolate by entering `myvar["donut"]["flavors"][0]`. We can display it by entering `print(myvar["donut"]["flavors"][0])`. We'll loop through and display the values too.

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
print("My favorite donut flavors are:", end=" ")

for f in myvar["donut"]["flavors"]:
  print(f, end=" ")
```

Let's look at a slightly more complex JSON structure such as:  `{"type": "donut", "flavors": {"flavor": [{"type" :"chocolate", "id": "1001"}, {"type": "glazed", "id": "1002"},{"type": "sprinkled", "id": "1003"}]}}`. In this case working from the inside out you should see that there are three objects nested in an array, and that this array is the value of the key flavor. The flavor key is part of an object that is the value of the key flavors. From the outside moving in, you see that both type and flavors are keys. As just mentioned the value of the key flavors is an object, and that object has the key flavor which has an array as its value that contains objects. First we assign this JSON structure to a variable `myvar1 = {"type": "donut", "flavors": {"flavor": [{"type": "chocolate", "id":"1001"}, {"type": "glazed", "id": "1002"},{"type": "sprinkled", "id": "1003"}]}}`. For each object we'll want to print the type and the id. We can access the value chocolate and its corresponding id by entering `myvar1["flavors"]["flavor"][0]["type"]` and `myvar1["flavors"]["flavor"][0]["id"]`. We can display it by entering `print("Id: " + str(myvar1["flavors"]["flavor"][0]["id"]) + " type: " + myvar1["flavors"]["flavor"][0]["type"])`. We'll loop through and display the values of id and type too.

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

for f in myvar1["flavors"]["flavor"]:
    print("Id is: " + str(f["id"]) + " type is: " + f["type"])
```

JSON Validation and Formatting
---

As you might have guessed if a JSON structure is being created a syntax error might be made making the structure difficult to parse. When creating a JSON structure you can validate your structure via websites or other tools.

For viewing purposes JSON is typically reformatted. The example above would typically look like the picture below, but is still parsed the same way.

```json
{
  "type": "donut",
  "flavors": [{
    "type": "chocolate",
    "id": "1001"
  }, {
    "type": "glazed",
    "id": "1002"
  }, {
    "type": "sprinkled",
    "id": "1003"
  }
}
```

### Script #10 - `10-json-nested-print.py`

El documento contiene multiples ejemplos de como imprimir los valores dentro de documentos de python. La idea es utilizando estos ejemplos, imprimir todos los valores de los últimos dos elementos de JSON.

#### Instrucciones

1. Ir al archivo `code/10-json-nested-print.py`.
2. Correr el script y estudiar el resultado.
3. Escribir el codigo necesario para imprimir todo el documento JSON y cada uno de sus valores individualmente.
4. Probar que el script corre correctamente.
