import json

def Scopes():
    with open("./config/scope.json") as server_scopes:
        server_scopes = json.load(server_scopes)
        prod = [
            server_scopes["Production_anna"],
            server_scopes["Production_sheep"]
        ]
        test = [
            server_scopes["Testing"]
        ]
        every = [
            server_scopes["Production_anna"],
            server_scopes["Production_sheep"],
            server_scopes["Testing"]
        ]
    return {"Production":prod, "Testing":test, "All":every}

# how to make `every=[prod, test]` but its `every=[**prod, **test]`