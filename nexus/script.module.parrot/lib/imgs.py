import requests
base = "https://images-ddg.pages.dev"

DB = requests.get("{}/list.json".format(base)).json()

def getIMG(id, type):
    try:
        path = DB[id]['urls'][type]
    except KeyError:
        path = DB['not-found']['urls'][type]
    return "{base}/{path}".format(base=base, path=path)
