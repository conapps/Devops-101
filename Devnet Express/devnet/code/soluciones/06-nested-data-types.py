"""
Script #6 - Nested data types
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

print("The second vegetable in the list is: " + FOOD["vegetables"][1])
print("The last dessert in the list is: " + FOOD["desserts"][2])

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

print("The Dodge sports model is: " + CARS["sports"]["Dodge"])
print("The classic Lincoln model is: " + CARS["classic"]["Lincoln"])
