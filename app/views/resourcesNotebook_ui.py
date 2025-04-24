import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
import os, subprocess, json 

from app.model.main_model import GetAllEntitiesModel
from app.settings import STATE, APPLICATION, LEVELS 

class ResourcesNotebook:

    def __init__(self, root, levels_file, entities_classes, scripts_dir):
        
        self.root = root 
        self.levels_file = levels_file
        self.entities_classes = entities_classes

        self.levels_file_json = LEVELS[0]
        
        self.resources_notebook = ttk.Notebook(self.root)
        self.resources_notebook.place(x=1, y=2, width=245, height=1890)  

        
        self.hierachy_tab = HierachyTab(root, self.levels_file, self.resources_notebook, self.entities_classes)
        # self.hierachy_tab = ProjectTab(root, self.entities_classes, self.resources_notebook)

        self.explorer_treeview = ExplorerTreeView(root, 'C:/Users/jerem/Desktop/asteroids/projects/asteroids_ECS/assets/')



        # el list box de los entities classes

        # self.listbox_entities = tk.Listbox(self.root, width=40, height=20)
        # self.listbox_entities.place(x=1, y=32)
    
    def new_script_popup(self):

        pass

class ExplorerTreeView():

    def __init__(self, root, directory):
        self.root = root
        self.directory = directory

        # Crear el Treeview
        self.tree = ttk.Treeview(root)
        self.tree.place(x=10, y=340, width=220, height=420)  

        # Configurar encabezados
        self.tree.heading("#0", text="Explorer", anchor="w")
        
        # Llenar el Treeview
        self.populate_tree(self.directory, "")

        
        # Asociar el evento de selección al Listbox
        self.tree.bind("<Double-1>", self.on_doubleclick_event)

    def on_doubleclick_event(self, event):
        """
        Maneja el evento de selección en el Treeview.
        """
        # Obtener el identificador del elemento seleccionado
        selected_item = self.tree.selection()
        
        if selected_item:

            # Obtener el texto del elemento seleccionado
            item_text = self.tree.item(selected_item[0], "text")
            # print(f"Elemento seleccionado: {item_text}")

            evaluate = self.evaluate_selection(item_text)

            if not evaluate:
                print(f"Carpeta: {item_text}")  

        else:
            print("No hay ningún elemento seleccionado.")

    def evaluate_selection(self, item):
        # verificar si la seleccion es un archivo o un directorio

        evaluate_item_type = item.split('.')

        # Evaluar si tiene mas de un elemento. 
        if len(evaluate_item_type) > 1:       
            if evaluate_item_type[1] == "py":
                self.open_script_on_editor(item)


        else:

            return False

    def open_script_on_editor(self, script_file):
        """
        Abre el archivo seleccionado en Visual Studio Code.
        """

        # Obtener el archivo de la lista usando el índice
        # file_name = self.scripts_listbox.get(script_file)
        dir = STATE.content['project_path'] + "\\assets\\scripts"
        file_path = os.path.join(dir, script_file)  # Ajustar con la ruta del directorio base
        
        try:
            # Abrir el archivo con Visual Studio Code
            subprocess.Popen(["code", file_path], shell=True)
 
        except FileNotFoundError:
            print(f"No se pudo abrir el archivo: {file_path}")

    def populate_tree(self, parent_path, parent_tree_id):
        """
        Llena el Treeview con los archivos y subdirectorios.
        Excluye cualquier directorio llamado 'py_cache' y cualquier archivo '__init__.py'.
        """
        try:
            # Iterar por el contenido del directorio
            for item in os.listdir(parent_path):
                item_path = os.path.join(parent_path, item)

                # Excluir directorios llamados 'py_cache'
                if item == "__pycache__" or item == "__init__.py":
                    continue

                # Comprobar si es un directorio
                if os.path.isdir(item_path):
                    # Añadir directorio al Treeview
                    folder_id = self.tree.insert(parent_tree_id, "end", text=item, open=False)
                    # Recursivamente añadir el contenido del subdirectorio
                    self.populate_tree(item_path, folder_id)
                else:
                    # Añadir archivo al Treeview
                    self.tree.insert(parent_tree_id, "end", text=item)
        except PermissionError:
            print(f"No se puede acceder a: {parent_path}")


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
        self.level_label.place(x=10, y=9)  # Empaquetar y añadir margen superior/inferior

        self.entity_listbox = tk.Listbox(self.level_tab, width=35, height=16)
        self.entity_listbox.place(x=10, y=32)

        self.contextual_menu = self.hierarchy_contextual_menu()

        for entity in self.entities:
            entity_name = entity['entity_name']
            self.entity_listbox.insert(tk.END, f"{entity_name}")
        
        self.notebook.add(self.level_tab, text="Level")

        self.entity_class_listbox()

        # Asociar el evento de selección al Listbox
        self.entity_listbox.bind("<<ListboxSelect>>", self.get_entity_details)

        
        APPLICATION.event_listener(self.root, "new entity form", "item added", self.insert_new_entity_to_listbox)

    def testing_events(self):

        trigger = "new-class-btn"
        type = "button click"
        data = {"msg":"Hola desde resources tab"}

        APPLICATION.add_event(trigger, type, data)

        # print(APPLICATION.events_queue)


    def get_entity_details(self, event):
        """
        Muestra la información de la entidad seleccionada.
        """
        # Obtener el índice del elemento seleccionado
        selected_index = self.entity_listbox.curselection()

        model = GetAllEntitiesModel()
        self.entities = model.get_all(LEVELS[0])
        
        if selected_index:  # Validar que no esté vacío
            # Buscar la entidad correspondiente
            

            entity = self.entities[selected_index[0]]
            
            print(f"Entidad seleccionada: {entity['entity_name']}")
            print(f"Detalles: {entity}")

            # Registrar evento
            trigger = "entities-listbox"
            type = "listbox element click"
            
            APPLICATION.add_event(trigger, type, entity)
        else:
            print("No hay ninguna entidad seleccionada.")

    def hierarchy_contextual_menu(self):
            ### menu contextual

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="New Entity", command=self.new_entity_event)

        # Vincular evento de clic derecho al menú contextual
        self.entity_listbox.bind("<Button-3>", self.show_context_menu)

        
        # self.listbox.bind("<<ListboxSelect>>", self.open_on_editor)
    
    def new_entity_event(self):

        # registrar evento. 
        trigger = "entities-contextual-menu"
        type = "new entity button click"
        
        entity=[]

        APPLICATION.add_event(trigger, type, entity)

        print(APPLICATION.events_queue)

    def entity_class_listbox(self):

        # # Crear los Frames que representarán el contenido de cada pestaña
        self.entity_classes_level_tab = ttk.Frame(self.notebook)
        
        self.entity_classes_level_label = tk.Label(self.level_tab, text="Classes", font=("Arial", 10))
        self.entity_classes_level_label.place(x=10, y=750)  # Empaquetar y añadir margen superior/inferior

        # create_button = tk.Button(self.level_tab, text="New Class", command=self.new_script_popup)
        # create_button.place(x=140, y=375)  # Ubicar el botón en la esquina derecha superior

        self.entity_classes_listbox = tk.Listbox(self.level_tab, width=35, height=11)
        self.entity_classes_listbox.place(x=10, y=770)

        
        for entity in self.entities_classes:
            entity_name = entity['class_name']
            APPLICATION.insert_element_on_listbox(self.entity_classes_listbox,tk,entity_name)
            # self.listbox.insert(tk.END, f"{entity_name}")
        
        # self.notebook.add(self.level_tab, text="Project")
        
        self.notebook.add(self.entity_classes_level_tab, text="Level")
    
    def open_on_editor(self, event):
        """
        Abre el archivo seleccionado en Visual Studio Code.
        """
        # Obtener el índice del archivo seleccionado
        selected_index = self.listbox.curselection()

        if selected_index:
            # Obtener el archivo de la lista usando el índice
            file_name = self.listbox.get(selected_index)
            file_path = os.path.join(self.scripts_dir, file_name)  # Ajustar con la ruta del directorio base
            
            try:
                # Abrir el archivo con Visual Studio Code
                subprocess.Popen(["code", file_path], shell=True)
                print(f"Abriendo archivo en VS Code: {file_path}")
            except FileNotFoundError:
                print(f"No se pudo abrir el archivo: {file_path}")

                
    def show_context_menu(self, event):
        """
        Muestra el menú contextual en las coordenadas del mouse.
        """
        self.context_menu.post(event.x_root, event.y_root)

    def insert_new_entity_to_listbox(self, event):
        # print(event)
        model = GetAllEntitiesModel()
        self.entities = model.get_all(LEVELS[0])
        print(self.entities)
        APPLICATION.insert_element_on_listbox(self.entity_listbox,tk,event["body"]["entity"])

class ProjectTab():

    def __init__(self, root, entities_classes, notebook):
        
        self.root = root 
        self.entities_classes = entities_classes
        self.notebook = notebook

        # # Crear los Frames que representarán el contenido de cada pestaña
        self.level_tab = ttk.Frame(self.notebook)
        
        self.level_label = tk.Label(self.level_tab, text="Classes", font=("Arial", 10))
        self.level_label.place(x=10, y=9)  # Empaquetar y añadir margen superior/inferior

        # create_button = tk.Button(self.level_tab, text="New Class", command=self.new_script_popup)
        # create_button.place(x=140, y=375)  # Ubicar el botón en la esquina derecha superior

        self.listbox = tk.Listbox(self.level_tab, width=40, height=16)
        self.listbox.place(x=1, y=32)

        
        for entity in self.entities_classes:
            entity_name = entity['class_name']
            self.listbox.insert(tk.END, f"{entity_name}")
        
        self.notebook.add(self.level_tab, text="Project")

    def new_script_popup(self):

        pass