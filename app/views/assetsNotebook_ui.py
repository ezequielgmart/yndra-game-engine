import tkinter as tk
from tkinter import ttk, messagebox

# from PIL import Image, ImageTk

# import os, subprocess, json 
from app.settings import STATE, APPLICATION 

class AssetsNotebook:
    
    def __init__(self, root, scripts_files):

        self.root = root
        self.scripts_files = scripts_files

        # Crear el Notebook
        self.assets_notebook = ttk.Notebook(self.root)
        self.assets_notebook.place(x=250, y=750, width=1367, height=400)

        self.edit_tab = EditTab(self.root, self.assets_notebook)
        self.viewer_tab = ViewerTab(self.root, self.assets_notebook)


        # tab2 = ttk.Frame(self.assets_tab)
        # tab4 = ttk.Frame(self.assets_tab)

        # # # Agregar las pestañas al Notebook
        # # self.assets_tab.add(self.scripts_frame, text="Scripts")
        # self.assets_tab.add(tab2, text="Images")
        # self.assets_tab.add(tab4, text="Sounds")
class ViewerTab: 

    def __init__(self, root, notebook):
        self.root = root
        self.notebook = notebook

        # Crear el Frame que contendrá los elementos
        self.main_frame = tk.Frame(self.notebook)
        self.main_frame.pack(fill="both", expand=True)

        # # Agregar la pestaña al Notebook
        self.notebook.add(self.main_frame, text="Viewer")


# tab donde poner forms
class EditTab:

    def __init__(self, root, notebook):
        self.root = root
        self.notebook = notebook

        self.childrens = []

        # Crear el Frame que contendrá los elementos
        self.main_frame = tk.Frame(self.notebook)
        self.main_frame.pack(fill="both", expand=True)

        # # Agregar la pestaña al Notebook
        self.notebook.add(self.main_frame, text="Edit")

        # Cargar las entidades en el Listbox
        # self.entities = levels_file['layers']['objects']['entities']  # Acceder a las entidades

        # APPLICATION.event_listener(self.root, "entities-contextual-menu", "new entity button click", self.create_new_entity_form)

    def testing(self, event):

        print("testing")

    def create_new_entity_form(self, event):

        """
        Crea el formulario dinámico en el inspector para la entidad dada.
        """

        ################### 
        self.form_frame = tk.Frame(self.main_frame, width=254, height=200)
        self.form_frame.place(x=0, y=0)
    
        form_title_label = tk.Label(self.form_frame, text="New Entity", font=("Arial", 11))
        form_title_label.place(x=5, y=5)

        
        name_title_label = tk.Label(self.form_frame, text="Name", font=("Arial", 9))
        name_title_label.place(x=5, y=35)

        # Textbox para mostrar el nombre de la entidad
        self.name_data_txt = tk.Text(self.form_frame, height=1, width=34, font=("Arial", 9))
        self.name_data_txt.place(x=45, y=35)
        
        add_entity_btn = tk.Button(self.form_frame, text="Add Entity", command=self.add_entity)
        add_entity_btn.place(x=45, y=65)  # Ubicar el botón en la esquina izquierda superior
        
        add_class_btn = tk.Button(self.form_frame, text="Add Class", command=self.add_class)
        add_class_btn.place(x=130, y=65)  # Ubicar el botón en la esquina izquierda superior


        self.childrens.append(self.form_frame)

    def add_class(self, event):

        pass 

    def add_entity(self):
        # Cargar los elementos del archivo JSON
        levels_json_file = APPLICATION.read_json_file(STATE.content['project_path'] + "\\assets\\levels\\initial_level.json")

        entities = levels_json_file['layers']['objects']['entities']
        new_entity = APPLICATION.new_entity_id(entities, self.name_data_txt)

        if new_entity is not None: 
            
            print(new_entity)

            self.clear_inspector()
            
            trigger = "new entity form"
            type = "item added"
            data = new_entity

            APPLICATION.add_event(trigger, type, data)
        else:
            print("Error")    

    def clear_inspector(self):
        """
        Borra los widgets anteriores del inspector.
        """
        for widget in self.childrens:

            widget.destroy()

        self.childrens = []
        # print(new_entity)

        # print(levels_file)

    # def event_listener(self, event_trigger, event_type, callback_function = None):
    #     """
    #     Revisa periódicamente la cola de eventos y los procesa.
    #     """
    #     if APPLICATION.events_queue:
    #         # Procesar los eventos en la cola
    #         for event in APPLICATION.events_queue[:]:  # Usamos una copia con slice
    #             if event["head"]["trigger"] == event_trigger and event["head"]["type"] == event_type:
    #                 # self.display_entity_components(event["body"])
                 
    #                 # Ejecutar la acción pasada como parámetro, si existe
    #                 if callback_function:
    #                     callback_function(event)

    #                 APPLICATION.events_queue.remove(event)  # Eliminar el evento después de procesarlo


    #     self.root.after(100, lambda: self.event_listener(event_trigger, event_type,callback_function))


    #     # # Cargar el ícono de script
        # script_icon = Image.open("data/py_icon.png")  # Cambia esta ruta por la de tu imagen
        # script_icon_image_resized = script_icon.resize((40, 40))  # Redimensionar la imagen
        # self.icon_photo = ImageTk.PhotoImage(script_icon_image_resized)

        # # Crear lista de elementos en la pestaña
        # icon_margin =20
        # script_name_margin = 10

        # for script in self.scripts_files:
        #     # Crear un Label para el ícono
        #     icon_label = tk.Label(self.scripts_frame, image=self.icon_photo)
        #     icon_label.place(x=icon_margin, y=25)

        #     # Crear un Label para el nombre con ajuste de texto
        #     script_label = tk.Label(self.scripts_frame, text=script, font=("Arial", 7), wraplength=70, justify="center")
        #     script_label.place(x=script_name_margin, y=70, width=70)  # Limitar el ancho del área

        #     # Aumentar el padding para los siguientes elementos
        #     icon_margin += 80
        #     script_name_margin += 80


class HierachyTab():

    def __init__(self, root, levels_file, notebook, entities_classes):
        
        self.root = root 
        self.levels_file = levels_file
        self.notebook = notebook
        self.entities_classes = entities_classes
        # # Crear los Frames que representarán el contenido de cada pestaña
        self.level_tab = ttk.Frame(self.notebook)

        # Cargar las entidades en el Listbox
        self.entities = levels_file['layers']['objects']['entities']  # Acceder a las entidades
        
        self.level_label = tk.Label(self.level_tab, text="Hierarchy", font=("Arial", 10))
        self.level_label.place(x=1, y=9)  # Empaquetar y añadir margen superior/inferior

        self.listbox = tk.Listbox(self.level_tab, width=35, height=16)
        self.listbox.place(x=10, y=32)

        self.contextual_menu = self.hierarchy_contextual_menu()

        for entity in self.entities:
            entity_name = entity['entity_name']
            self.listbox.insert(tk.END, f"{entity_name}")
        
        self.notebook.add(self.level_tab, text="Level")
