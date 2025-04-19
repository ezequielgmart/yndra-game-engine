from app.model.main_model import AppModel
import time
import hashlib



class AppController(AppModel):

    def __init__(self):

        super().__init__()


class AppState(AppModel):

    def __init__(self, project_json):

        super().__init__()
        self.json_file = project_json
        self.content = self.read_json_file(self.json_file)


    def add_project(self, project_dir):

        self.update_json_data(self.json_file, project_name=None, project_path=project_dir)


# la clase que se encargara de registrar los eventos y comunicarlos entre componentes de la ui
class Application(): 

    def __init__(self):

        self.events_queue = []
    
    def create_event(self, trigger, type, data): 
        # trigger : Componente que ingreso el evento en el queue 
        event = {
            "head": {
                "id": self.create_id(),
                "type": type,  # Esto define correctamente el tipo
                "trigger": trigger  # Cambié 'type' por 'trigger' para evitar sobrescritura
            },
            "body": data
        }

        return event
    
    def add_event(self, trigger, type, data): 

        """
        
        """
        event = self.create_event(trigger, type, data)

        self.events_queue.append(event) 

    def remove_event(self, event):
        
        for item in self.events_queue:
            if item["head"]["id"] ==  event["head"]["id"]:
                
                self.events_queue.remove(item)

                return True

    def create_id(self):

            # Obtener la fecha actual en formato Unix
            current_time_unix = int(time.time())
            # Convertir la fecha en un hash (SHA-256)
            hash_object = hashlib.sha256(str(current_time_unix).encode())
            hash_hex = hash_object.hexdigest()

            return hash_hex

