"""
Script #9 - JSON print.
"""

VAR = {
    "car": "volvo",
    "fruit": "apple"
}

print(VAR["fruit"])

for value in VAR:
    print("key: " + value + " value: " + VAR[value])

print()
print()

VAR1 = {
    "donut": [
        "chocolate",
        "glazed",
        "sprinkled"
    ]
}

print(VAR1["donut"][0])

print("My favorite donut flavors are:", end=" ")

for f in VAR1["donut"]:
    print(f, end=" ")

print()
print()

VAR2 = {
    "vegetable": "carrot",
    "fruit": "apple",
    "animal": "cat",
    "day": "Friday"
}

VAR3 = {
    "animal": [
        "dog",
        "cat",
        "fish",
        "tiger",
        "camel"
    ]
}

# 1. Imprimir todos los valores incluidos en los JSONs declarados.
