import json

"""

Componente del motor para generar los datos principales que se necesita para que 
el juego funcione. 

algunos metodos que se puede utilizar a lo largo del motor

"""

def read_json_file(json_file):

    with open(json_file, "r") as f:
        data = json.load(f)

    return data