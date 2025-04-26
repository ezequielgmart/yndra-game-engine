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
            




class NewEntityModel:

    def __init__(self, json_file, entity_id, entity_name):
        self.json_file = json_file
        self.entity_id = entity_id
        self.entity_name = entity_name

    def add_item(self):    
        # Leer el archivo JSON
        with open(self.json_file, 'r') as file:
            data = json.load(file)

        # Nuevo elemento que deseas agregar
        new_entity = {
            'entity_id': self.entity_id,  # Cambia el ID según sea necesario
            'entity_name': self.entity_name,
            'components': []
        }

        # Agregar el nuevo elemento al JSON en "entities" dentro de "objects"
        data['layers']['objects']['entities'].append(new_entity)

        # Guardar el archivo actualizado
        with open(self.json_file, 'w') as file:
            json.dump(data, file, indent=4)

        return new_entity

class GetAllEntitiesModel: 

    def __init__(self):

        # lista de todos los entitys
        self.data = []
        
    def get_all(self, file):

        model = AppModel().read_json_file(file)     
        data = model['layers']['objects']['entities'] 

        return data
    
class GetAllLevelData:
    
    def __init__(self):

        # lista de todos los entitys
        self.data = []
        
    def get_all(self, file):

        data = AppModel().read_json_file(file)     

        return data



class UpdateEntity:

    def __init__(self):
        pass

    
    def save_level_data(self, level_file_path, new_entity_data):
        """Guarda la estructura de datos del nivel de vuelta al archivo JSON."""
        # path = "C://Users//jerem//Desktop//asteroids//projects//asteroids_ECS//assets//levels//initial_level.json"
        try:
            with open(level_file_path, 'w') as f:
                json.dump(new_entity_data, f, indent=4)
        except Exception as e:
            print(f"Error al guardar los datos del nivel: {e}")

class DeleteEntityModel: 

    def __init__(self):
        pass

    def delete_by_name(self, level_file_path, entity_name_to_delete):
            try:
                with open(level_file_path, 'r') as f:
                    data = json.load(f)

                if 'layers' in data and 'objects' in data['layers'] and 'entities' in data['layers']['objects'] and isinstance(data['layers']['objects']['entities'], list):
                    initial_entity_count = len(data['layers']['objects']['entities'])
                    data['layers']['objects']['entities'] = [
                        entity for entity in data['layers']['objects']['entities']
                        if entity.get('entity_name') != entity_name_to_delete
                    ]
                    final_entity_count = len(data['layers']['objects']['entities'])

                    if initial_entity_count > final_entity_count:
                        with open(level_file_path, 'w') as f:
                            json.dump(data, f, indent=2)
                        # print(f"Entidad con nombre '{entity_name_to_delete}' eliminada de {level_file_path}")
                        response_code = {
                            "code":200,
                            "msg":f"Entidad con nombre '{entity_name_to_delete}' eliminada de {level_file_path}"
                        } 
                        return response_code
                    else:
                        # print(f"No se encontró ninguna entidad con el nombre '{entity_name_to_delete}' en {level_file_path}")
                        
                        response_code = {
                            "code":500,
                            "msg":f"No se encontró ninguna entidad con el nombre '{entity_name_to_delete}' en {level_file_path}"
                        } 

                        return response_code

                else:
                    # print()

                        response_code = {
                            "code":400,
                            "msg":f"La estructura del archivo JSON en {level_file_path} no es la esperada para eliminar entidades."
                        } 

                        return response_code

            except FileNotFoundError:

                print(f"El archivo {level_file_path} no fue encontrado.")

            except json.JSONDecodeError:
                
                print(f"Error al decodificar el JSON en {level_file_path}.")