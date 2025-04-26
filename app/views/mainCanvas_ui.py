import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from app.settings import STATE, APPLICATION, LEVELS
from app.model.main_model import GetAllEntitiesModel, UpdateEntity, GetAllLevelData

class MainCanvas:

    def __init__(self, root, project_file_data):

        self.root = root
        self.project_file_data = project_file_data

        # Inicializa self.level_data con los datos del proyecto
        self.level_data = GetAllLevelData().get_all(LEVELS[0])
        # print("Initial level data:", self.level_data) # Para depuración

        self.level_designer_tab = ttk.Notebook(self.root)
        self.level_designer_tab.place(x=250, y=30, width=1367, height=850)

        # Crear el Frame para la pestaña
        self.designer_frame = tk.Frame(self.level_designer_tab, width=1360, height=590)
        self.designer_frame.pack(fill="both", expand=True)

        # Cargar la imagen
        canvas_img = Image.open("data/canvas-bg.png")  # Cambia esta ruta por la de tu imagen
        image_resized = canvas_img.resize((1360, 850))  # Redimensionar la imagen
        self.photo = ImageTk.PhotoImage(image_resized)

        # Crear un Label para la imagen dentro del Frame
        self.image_label = tk.Label(self.designer_frame, image=self.photo)
        self.image_label.place(x=0, y=0)  # Posicionar la imagen al inicio del Frame

        # Crear el Frame adicional encima de la imagen
        self.canvas_frame = tk.Frame(self.designer_frame, bg="black", width=self.project_file_data["width"], height=self.project_file_data["height"], borderwidth=5)
        self.canvas_frame.place(x=int(1360*0.2), y=int(590*0.1))  # Posicionar el Frame en coordenadas relativas dentro de designer_frame

        # Agregar la pestaña al Notebook
        self.level_designer_tab.add(self.designer_frame, text="Designer")

        self.entities_on_scene = []
        self.entity_updater = UpdateEntity() # Instancia UpdateEntity

        self.hierarchy_contextual_menu() # <--- Llama a la función para crear el menú contextual

        # Vincular evento de clic derecho al menú contextual del designer_frame
        self.designer_frame.bind("<Button-3>", self.show_context_menu)

        # Vincular evento de clic derecho al menú contextual de la image_label (la imagen de fondo)
        self.image_label.bind("<Button-3>", self.show_context_menu)

        
        # Vincular evento de clic derecho al menú contextual de la image_label (la imagen de fondo)
        self.canvas_frame.bind("<Button-3>", self.show_context_menu)

        self.render_entities()


    def render_entities(self):
        model = GetAllEntitiesModel()
        self.entities = model.get_all(LEVELS[0])

        for entity in self.entities:
            for component in entity["components"]:
                if component["type"] == "Render":
                    img_path = os.path.join(STATE.content['project_path'] + "\\" + component["data"]['sprites'])
                    x = entity["components"][0]["data"]["x"]
                    y = entity["components"][0]["data"]["y"]
                    entity_representation = EntityRender(self.designer_frame, img_path, x, y, entity, self.update_entity_data, self.entity_updater, self.level_data) # Pasa self.update_entity_data y self.entity_updater
                    self.entities_on_scene.append(entity_representation)


    def update_entity_data(self, entity_name, new_x, new_y):
        """Actualiza la posición de la entidad directamente en self.level_data."""
        if isinstance(self.level_data, dict) and "layers" in self.level_data:
            for layer_name, layer_data in self.level_data["layers"].items():
                if isinstance(layer_data, dict) and "entities" in layer_data:
                    for entity_data in layer_data["entities"]:
                        if entity_data["entity_name"] == entity_name:
                            for i, component in enumerate(entity_data["components"]):
                                if component["type"] == "Position":
                                    entity_data["components"][i]["data"]["x"] = new_x
                                    entity_data["components"][i]["data"]["y"] = new_y
                                    return
                else:
                    print(f"Advertencia: La capa '{layer_name}' no tiene la clave 'entities' o no es un diccionario.")
        else:
            print("Error: self.level_data no tiene la clave 'layers' o no es un diccionario.")

    def hierarchy_contextual_menu(self):
        ### menu contextual

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="New Entity", command=self.new_entity_event)


    def new_entity_event(self):

        # registrar evento.
        trigger = "entities-contextual-menu"
        type = "new entity button click"

        entity=[]

        APPLICATION.add_event(trigger, type, entity)

        print(APPLICATION.events_queue)


    def show_context_menu(self, event):
        """
        Muestra el menú contextual en las coordenadas del mouse.
        """
        self.context_menu.post(event.x_root, event.y_root)

class EntityRender:
    def __init__(self, frame_container, img_path, x, y, entity, update_callback, entity_updater, level_data): # Recibe entity_updater

        try:
            self.entity = entity
            self.imagen_sprite = tk.PhotoImage(file=img_path)
            self.image_label = tk.Label(frame_container, image=self.imagen_sprite, bg="black")
            self.image_label.image = self.imagen_sprite
            self.initial_x = int(1360 * 0.2) + x
            self.initial_y = int(590 * 0.1) + y
            self.image_label.place(x=self.initial_x, y=self.initial_y)

            self.dragging = False
            self.drag_start_x = 0
            self.drag_start_y = 0
            self.update_callback = update_callback # Recibe la función de actualización
            self.entity_updater = entity_updater # Guarda la instancia de UpdateEntity
            self.level_data = level_data # Recibe la referencia a self.level_data

            self.image_label.bind("<ButtonPress-1>", self.on_drag_start)
            self.image_label.bind("<Motion>", self.on_drag_motion)
            self.image_label.bind("<ButtonRelease-1>", self.on_drag_release)
            # self.image_label.bind("<Double-Button-1>", self.on_label_doubleclick)

        except tk.TclError as e:
            print(f"Error al cargar la imagen: {img_path} - {e}")

    def on_drag_start(self, event):
        self.dragging = True

        self.get_entity_details(event)

        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.image_label.config(cursor="hand2")

    def on_drag_motion(self, event):
        if self.dragging:
            delta_x = event.x - self.drag_start_x
            delta_y = event.y - self.drag_start_y
            new_x = self.image_label.winfo_x() + delta_x
            new_y = self.image_label.winfo_y() + delta_y
            self.image_label.place(x=new_x, y=new_y)

    def on_drag_release(self, event):
        self.dragging = False
        self.image_label.config(cursor="")

        final_x_relative = self.image_label.winfo_x() - int(1360 * 0.2)
        final_y_relative = self.image_label.winfo_y() - int(590 * 0.1)

        # Llamar a la función de actualización en MainCanvas
        if self.update_callback:
            self.update_callback(self.entity["entity_name"], final_x_relative, final_y_relative)

        # Llama a la función de guardar usando la instancia de UpdateEntity
        self.entity_updater.save_level_data(LEVELS[0],self.level_data)

    def on_label_doubleclick(self, event):
        self.get_entity_details(event)

    def get_entity_details(self, event):
        model = GetAllEntitiesModel()
        entities = model.get_all(LEVELS[0])
        for item in entities:
            if item["entity_name"] == self.entity["entity_name"]:
                print(f"Entidad seleccionada: {item['entity_name']}")
                trigger = "entities-listbox"
                type = "listbox element click"
                APPLICATION.add_event(trigger, type, item)
                break
 