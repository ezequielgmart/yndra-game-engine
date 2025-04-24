
import time
import hashlib
import json, os

from tkinter import messagebox

from app.model.main_model import AppModel, NewEntityModel



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

    def event_listener(self, root, event_trigger, event_type, callback_function = None):
        """
        Revisa periódicamente la cola de eventos y los procesa.
        """
        if self.events_queue:
            # Procesar los eventos en la cola
            for event in self.events_queue[:]:  # Usamos una copia con slice
                if event["head"]["trigger"] == event_trigger and event["head"]["type"] == event_type:
                    # self.display_entity_components(event["body"])
                
                    # Ejecutar la acción pasada como parámetro, si existe
                    if callback_function:
                        callback_function(event)

                    self.events_queue.remove(event)  # Eliminar el evento después de procesarlo

        root.after(100, lambda: self.event_listener(root, event_trigger, event_type,callback_function))

    def insert_element_on_listbox(self, listbox, tkinter, item):

        listbox.insert(tkinter.END, f"{item}")

        
    def read_json_file(self, json_file):
        with open(json_file, "r") as f:
            data = json.load(f)
        return data

    def new_entity_id(self, entities_list, name_data_txt):
        # Encuentra el mayor valor de "entity_id" en la lista
        new_id = max(entities_list, key=lambda x: x["entity_id"])["entity_id"]
        new_id += 1

        # Obtener el texto del Textbox
        entity_name = name_data_txt.get("1.0", "end").strip()  # Eliminar espacios y salto de línea

        # Validar si el nombre no está vacío
        if not entity_name:
            self.show_warning("Entity name missing!")
            return None  # Salir de la función si está vacío

        # Comprobar que el nombre no se encuentre
        for entity in entities_list:
            if entity_name == entity["entity_name"]:
                self.show_warning("Already exist!")
                return None  # Salir de la función si ya existe

        # Si pasó todas las validaciones, devolver el resultado
        result = {"id": new_id, "entity": entity_name}

        level_json_file = "C:\\Users\\jerem\\Desktop\\asteroids\\projects\\asteroids_ECS\\assets\\levels\\initial_level.json"

        if result is not None:

            new_entity_model = NewEntityModel(level_json_file, result["id"], result["entity"])

            query_result = new_entity_model.add_item()
            
        return result


    
    def show_warning(self, warning_msg):
        messagebox.showwarning("Warning!", warning_msg)    


