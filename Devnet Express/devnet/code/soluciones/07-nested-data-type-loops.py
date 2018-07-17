"""
Script #7 - Nested data type loops.
"""

FOOD = {
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

for vegetable in FOOD["vegetables"]:
    print("My favorite vegetable is " + vegetable)

for dessert in FOOD["desserts"]:
    print("My favorite dessert is " + dessert)

CARS = {
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

for auto in CARS["sports"]:
    print("My favorite sports car make and model is the " + auto + " " + CARS["sports"][auto])

for auto in CARS["classic"]:
    print("My favorite classic car make and model is the " + auto + " " + CARS["classic"][auto])
