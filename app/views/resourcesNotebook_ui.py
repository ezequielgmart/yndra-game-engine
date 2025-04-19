import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
import os, subprocess, json 
from app.settings import STATE, APPLICATION 

class ResourcesNotebook:

    def __init__(self, root, levels_file, entities_classes, scripts_dir):
        
        self.root = root 
        self.levels_file = levels_file
        self.entities_classes = entities_classes

        
        self.resources_notebook = ttk.Notebook(self.root)
        self.resources_notebook.place(x=1, y=2, width=245, height=1890)  

        
        self.hierachy_tab = HierachyTab(root, self.levels_file, self.resources_notebook, self.entities_classes)
        self.hierachy_tab = ProjectTab(root, self.entities_classes, self.resources_notebook)



        # el list box de los entities classes

        # self.listbox_entities = tk.Listbox(self.root, width=40, height=20)
        # self.listbox_entities.place(x=1, y=32)
    
    def new_script_popup(self):

        pass


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

        create_button = tk.Button(self.level_tab, text="New Class", command=self.testing_events)
        create_button.place(x=140, y=375)  # Ubicar el botón en la esquina derecha superior

        self.listbox = tk.Listbox(self.level_tab, width=40, height=16)
        self.listbox.place(x=1, y=32)

        self.contextual_menu = self.hierarchy_contextual_menu()

        for entity in self.entities:
            entity_name = entity['entity_name']
            self.listbox.insert(tk.END, f"{entity_name}")
        
        self.notebook.add(self.level_tab, text="Level")


        # Asociar el evento de selección al Listbox
        self.listbox.bind("<<ListboxSelect>>", self.get_entity_details)

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
        selected_index = self.listbox.curselection()

        if selected_index:
            # Buscar la entidad correspondiente
            entity = self.entities[selected_index[0]]
            
            # print(f"Entidad seleccionada: {entity['entity_name']}")
            # print(f"Detalles: {entity}")

            # registrar evento. 
            trigger = "entities-listbox"
            type = "listbox element click"
            


            APPLICATION.add_event(trigger, type, entity)
            
        else:
            print("No hay ninguna entidad seleccionada.")

    def hierarchy_contextual_menu(self):
            ### menu contextual

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="New Entity", command=self.open_on_editor)

        # Vincular evento de clic derecho al menú contextual
        self.listbox.bind("<Button-3>", self.show_context_menu)

        
        self.listbox.bind("<<ListboxSelect>>", self.open_on_editor)
        
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

class ProjectTab():

    def __init__(self, root, entities_classes, notebook):
        
        self.root = root 
        self.entities_classes = entities_classes
        self.notebook = notebook

        # # Crear los Frames que representarán el contenido de cada pestaña
        self.level_tab = ttk.Frame(self.notebook)
        
        self.level_label = tk.Label(self.level_tab, text="Classes", font=("Arial", 10))
        self.level_label.place(x=1, y=9)  # Empaquetar y añadir margen superior/inferior

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