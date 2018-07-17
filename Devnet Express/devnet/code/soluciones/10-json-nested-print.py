"""
Script #10 - JSON nested print.
"""

VAR = {
    "donut": {
        "flavors": [
            "chocolate",
            "jelley",
            "maple",
            "plain"
        ]
    }
}

print(VAR["donut"]["flavors"][0])
print("My favorite donut flavors are:", end=" ")

for flavor in VAR["donut"]["flavors"]:
    print(flavor, end=" ")

print()
print()

VAR1 = {
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

print(
    "Id: "
    + str(VAR1["flavors"]["flavor"][0]["id"])
    + " type: "
    + VAR1["flavors"]["flavor"][0]["type"]
)

for f in VAR1["flavors"]["flavor"]:
    print("Id: " + str(f["id"]) + " type: " + f["type"])

print()

print()

# 1. Imprimir todos los valores incluidos en los JSONs declarados.

VAR3 = {
    "exercise": {
        "high impact": [
            "running",
            "jumping",
            "jump rope",
            "running down stairs",
            "skiing"
        ]
    }
}

VAR4 = {
    "author": "Stephen King",
    "famous works": {
        "novels": [{
            "title": "The Shining",
            "id": 1001
        }, {
            "title": "Carrie",
            "id": 1002
        }, {
            "title": "It",
            "id": 1003
        }, {
            "title": "Misery",
            "id": 1004
        }, {
            "title": "Night Shift",
            "id": 1005
        }]
    }
}

print(VAR3)

for first_variable in VAR3:
    print(first_variable, "{")
    for second_variable in VAR3[first_variable]:
        print(" ", second_variable, "{")
        for third_variable in VAR3[first_variable][second_variable]:
            print("   ", third_variable)
        print("  }")
    print("}\n")

print(VAR4)

for first_variable in VAR4:
    if first_variable == "author":
        print(first_variable, ":", VAR4[first_variable])
    else:
        print(first_variable, "{")
        for second_variable in VAR4[first_variable]:
            print(" ", second_variable, "{")
            for third_variable in VAR4[first_variable][second_variable]:
                for fourth_variable in third_variable:
                    print(
                        "  ",
                        fourth_variable,
                        ":",
                        str(third_variable[fourth_variable])
                    )
