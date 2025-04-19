import json, os

class AppModel:

    def __init__(self):

        pass

    def read_json_file(self,json_file):

        with open(json_file, "r") as f:
            data = json.load(f)

        return data
    
    def get_project_name(self,path):
        # Obtener el último nombre de la ruta
        dir_name = os.path.basename(path)
        return dir_name 
    
    def update_json_data(self, json_file, project_name=None, project_path=None):
        """
        Actualiza los datos del archivo JSON con el nombre y la ruta del proyecto.
        
        Args:
            project_name (str): El nombre del proyecto a agregar o actualizar.
            project_path (str): La ruta del proyecto a agregar o actualizar.
        """
        # Cargar el contenido actual del archivo JSON
        with open(json_file, "r") as file:
            data = json.load(file)

        # Agregar o actualizar los datos proporcionados
        
            data["project_name"] = self.get_project_name(project_path)
            data["project_path"] = project_path

        # Guardar los cambios en el archivo JSON
        with open(self.json_file, "w") as file:
            json.dump(data, file, indent=4)
    