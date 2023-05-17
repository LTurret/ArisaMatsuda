import json

def scopes() -> list:
    with open("./core/config/scope.json", "r") as scope:
        scope = json.load(scope)

        anna = scope["Production_anna"]
        arisa = scope["Production_arisa"]
        testing = scope["Testing"]

    prod = [anna, arisa]
    test = [testing]
    every = [anna, arisa, testing]

    serverSet = {
        "anna": anna,
        "arisa": arisa,
        "prod": prod,
        "testing": test,
        "all": every
    }

    return serverSet