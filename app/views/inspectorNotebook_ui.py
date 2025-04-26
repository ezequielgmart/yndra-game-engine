import tkinter as tk
from tkinter import ttk
import os, subprocess
from PIL import Image, ImageTk
# import os, subprocess, json 
from app.settings import STATE, APPLICATION

class InspectorNotebook:

    def __init__(self, root, levels_file, scripts_dir):
        self.notebook_width = 295
        self.root = root
        self.levels_file = levels_file
        self.childrens = []
        self.scripts_dir = scripts_dir

        self.inspector_notebook = ttk.Notebook(self.root)
        self.inspector_notebook.place(x=1620, y=0, width=self.notebook_width , height=1100)  
        
        # # Crear los Frames que representarán el contenido de cada pestaña
        self.inspector_tab = ttk.Frame(self.inspector_notebook)

        # # Asociar evento para mostrar el id de la entidad seleccionada
        # self.listbox_entities.bind("<<ListboxSelect>>", self.show_entity_details)

        self.inspector_notebook.add(self.inspector_tab, text="inspector")

        # self.check_events()
        APPLICATION.event_listener(self.root, "entities-listbox", "listbox element click", self.display_entity_components)
        
        APPLICATION.event_listener(self.root, "entities-contextual-menu", "new entity button click", self.create_new_entity_form)

    def new_entity_popup(self):
        """
        Abre una ventana emergente.
        """
        new_entity_popup = tk.Toplevel(self.root)
        new_entity_popup.title("Entity Form")
        new_entity_popup.geometry("300x200")

        self.label = tk.Label(new_entity_popup, text="New entity", font=("Arial", 14))
        self.label.place(x=10, y=5)  
        
        self.label = tk.Label(new_entity_popup, text="Name", font=("Arial", 10))
        self.label.place(x=10, y=60)  

        self.entry_entity_name = tk.Entry(new_entity_popup, width=30)
        self.entry_entity_name.place(x=10, y=80) 
        self.entry_entity_name.insert(0, "")  # Texto por defecto

        create_button = tk.Button(new_entity_popup, text="Create", command=self.create_new_script_file)
        create_button.place(x=10, y=100) 


    def display_entity_components(self, entity):
        """
        Crea el formulario dinámico en el inspector para los componentes de la entidad o clase.
        """
        entity_data = entity["body"]

        if len(self.childrens) > 0:

            self.clear_inspector()  # Limpiar el inspector antes de mostrar nuevos widgets
        # self.create_inspector_form(entity_data)
        
        self.create_inspector_form(entity_data)


    def create_new_script_file(self):
        file_name = self.entry.get() + ".py"  
        directory = STATE.content['project_path'] + "//assets//scripts"
        if self.entry.get() == "":
            print("New file without a name")
            return
        if os.path.isdir(directory):
            file_path = os.path.join(directory, file_name)
            try:
                with open(file_path, 'w') as file:
                    file.write(f"""

class {self.entry.get()}:

    def __init__(self, entity):
        \"\"\"
        Almacena la entidad asociada.
        \"\"\"
        self.entity = entity

    def update(self, events):
        \"\"\"
        Actualiza el estado de la entidad
        \"\"\"
        pass
""")
                

                APPLICATION.insert_element_on_listbox(self.listbox, tk, file_name)

                self.entry.delete(0, tk.END)
            except Exception as e:
                print(f"Error al crear el archivo: {e}")
        else:
            print("La ruta especificada no es válida.")

    def clear_inspector(self):
        """
        Borra los widgets anteriores del inspector.
        """
        for widget in self.childrens:

            widget.destroy()

        self.childrens = []
        """Elimina el label dentro del frame."""
    def create_inspector_form(self, entity):    
        """
        Crea el formulario dinámico en el inspector para la entidad dada.
        """
    
        self.clear_inspector() 
        ################### 
        self.entity_info_frame  = tk.Frame(self.inspector_tab, width=self.notebook_width, height=60)
        self.entity_info_frame.place(x=0, y=0)

        self.close_inspector_btn = tk.Button(self.entity_info_frame, text="X", command=self.clear_inspector)
        self.close_inspector_btn.place(x=260, y=5) 

        
        self.delete_entity_btn = tk.Button(self.entity_info_frame, text="Delete", command=self.scripts_contextual_menu)
        self.delete_entity_btn.place(x=10, y=100) 

        # Textbox para mostrar el nombre de la entidad
        name_data_txt = tk.Text(self.entity_info_frame, height=1, width=34, font=("Arial", 10))
        name_data_txt.place(x=5, y=5)
        name_data_txt.insert(tk.END, entity["entity_name"])  # Insertamos el texto inicial
        name_data_txt.config(state=tk.DISABLED)  # Hacemos el textbox de solo lectura

        self.childrens.append(self.entity_info_frame)

        
        for component in entity["components"]:

            if component["type"] == "Position":

                self.position_model = entity["components"][0]["data"]
                # *** POSITION ************ #  
                self.position_component_frame = tk.Frame(self.inspector_tab, width=self.notebook_width, height=100, bd=1, relief="groove")
                self.position_component_frame.place(x=0, y=36)

                # Primer Label: "Position"
                self.position_label = tk.Label(self.position_component_frame, text="Position", font=("Arial", 8))
                self.position_label.place(x=5, y=5)  # Dejamos un pequeño margen desde la esquina superior izquierda

                #### Coordenadas ajustadas desde el Label "Position"
                base_y_offset = 30  # Espacio vertical que queremos dejar debajo del "Position"
                label_col_1 = 5     # Columna izquierda
                label_col_2 = 150   # Columna derecha
                label_row_1 = base_y_offset + 5  # Primera fila ajustada según el margen
                label_row_2 = base_y_offset + 40  # Segunda fila ajustada según el margen

                textbox_col_1 = 50  # Columna izquierda
                textbox_col_2 = 200 # Columna derecha
                textbox_row_1 = base_y_offset + 5  # Fila superior ajustada
                textbox_row_2 = base_y_offset + 40  # Fila inferior ajustada
                textbox_width = 8



                # Esquina superior izquierda: X
                self.x_label = tk.Label(self.position_component_frame, text="X", font=("Arial", 8))
                self.x_label.place(x=label_col_1, y=label_row_1)
                x_data_txt = tk.Text(self.position_component_frame, height=1, width=textbox_width, font=("Arial", 8))
                x_data_txt.place(x=textbox_col_1, y=textbox_row_1)
                x_data_txt.insert(tk.END, self.position_model['x'])

                # Esquina superior derecha: Y
                self.y_label = tk.Label(self.position_component_frame, text="Y", font=("Arial", 8))
                self.y_label.place(x=label_col_2, y=label_row_1)
                y_data_txt = tk.Text(self.position_component_frame, height=1, width=textbox_width, font=("Arial", 8))
                y_data_txt.place(x=textbox_col_2, y=textbox_row_1)
                y_data_txt.insert(tk.END, self.position_model['y'])

                # Esquina inferior izquierda: Scale
                self.scale_label = tk.Label(self.position_component_frame, text="Scale", font=("Arial", 8))
                self.scale_label.place(x=label_col_1, y=label_row_2)
                scale_data_txt = tk.Text(self.position_component_frame, height=1, width=textbox_width, font=("Arial", 8))
                scale_data_txt.place(x=textbox_col_1, y=textbox_row_2)
                scale_data_txt.insert(tk.END, self.position_model['scale'])

                # Esquina inferior derecha: Rotation
                self.rotation_label = tk.Label(self.position_component_frame, text="Rotation", font=("Arial", 8))
                self.rotation_label.place(x=label_col_2, y=label_row_2)
                rotation_data_txt = tk.Text(self.position_component_frame, height=1, width=textbox_width, font=("Arial", 8))
                rotation_data_txt.place(x=textbox_col_2, y=textbox_row_2)
                rotation_data_txt.insert(tk.END, self.position_model['rotation'])

                # Agregar el Frame al contenedor de hijos
                self.childrens.append(self.position_component_frame)


            elif component["type"] == "Render":
                # *** RENDER ************ #  
                ################################ 
                self.render_model = entity["components"][1]["data"]
                

                # Calculamos la nueva posición para el siguiente frame (debajo de position_component_frame)
                render_frame_y = 36 + 100 + 10  # Altura del position_component_frame (100) más un margen de 10 píxeles

                self.render_component_frame = tk.Frame(self.inspector_tab, width=self.notebook_width, height=200, bd=1, relief="groove")
                self.render_component_frame.place(x=0, y=render_frame_y)  # Posicionamos este frame debajo del anterior

                
                # Primer Label: "Position"
                self.render_label = tk.Label(self.render_component_frame, text="Render", font=("Arial", 8))
                self.render_label.place(x=5, y=5)  # Dejamos un pequeño margen desde la esquina superior izquierda

                # Dentro del frame render_component_frame, cargar la imagen del background
                src_bg = "data/img-bg.jpg"
                bg_img = Image.open(src_bg)  # Cambia esta ruta por la de tu imagen
                bg_img_resized = bg_img.resize((150, 150))  # Redimensionar la imagen
                self.bg_photo = ImageTk.PhotoImage(bg_img_resized)

                # Crear un Label para mostrar la imagen en el render frame
                bg_img_label = tk.Label(self.render_component_frame, image=self.bg_photo)
                bg_img_label.place(x=5, y=30)  # Ajustar coordenadas dentro del frame

                # self.childrens.append(bg_img_label)

                # Cargar la imagen del entity
                src_entity =os.path.join(STATE.content['project_path'],self.render_model["sprites"]) 

                entity_img = Image.open(src_entity)  # Cambia esta ruta por la de tu imagen
                entity_img_resized = entity_img.resize((85, 85))  # Redimensionar la imagen
                self.entity_photo = ImageTk.PhotoImage(entity_img_resized)

                # Crear un Label para mostrar la imagen del entity dentro del render frame
                entity_img_label = tk.Label(self.render_component_frame, image=self.entity_photo)
                entity_img_label.place(x=40, y=60)  # Ajustar la posición dentro del frame

                self.childrens.append(self.render_component_frame)

            elif component["type"] == "behaviour":
                
                # self.behaviour_model = entity["components"][2]["data"]

                self.behaviour_model = entity["components"][2]["data"]
                

                # Calculamos la nueva posición para el siguiente frame (debajo de position_component_frame)
                behaviour_frame_y = 236 + 100 + 10  # Altura del position_component_frame (100) más un margen de 10 píxeles

                self.behaviour_component_frame = tk.Frame(self.inspector_tab, width=self.notebook_width, height=350, bd=1, relief="groove")
                self.behaviour_component_frame.place(x=0, y=behaviour_frame_y)  # Posicionamos este frame debajo del anterior

                
                # Title Label: 
                self.behaviour_label = tk.Label(self.behaviour_component_frame, text="Behaviour", font=("Arial", 8))
                self.behaviour_label.place(x=5, y=5)  # Dejamos un pequeño margen desde la esquina superior izquierda

                
                self.scripts_listbox = tk.Listbox(self.behaviour_component_frame, width=40, height=16)
                self.scripts_listbox.place(x=15, y=32)


                for script in self.behaviour_model['scripts']:

                    module= script['module']
                    self.scripts_listbox.insert(tk.END, f"{module}")

                
                # Asociar el evento de selección al Listbox
                self.scripts_listbox.bind("<Double-1>", self.open_on_editor)

                
                self.scripts_listbox.bind("<<ListboxSelect>>", self.listbox_item_contextual_menu)

                self.contextual_menu = self.scripts_contextual_menu()

                
                self.childrens.append(self.behaviour_component_frame)

    def listbox_item_contextual_menu(self, event):

        selected_index = self.scripts_listbox.curselection()

        if selected_index:

            name = self.scripts_listbox.get(selected_index)

            print(name)



    def scripts_contextual_menu(self):
            ### menu contextual

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="New script", command=self.new_script_popup)

        
        # Vincular evento de clic derecho al menú contextual
        self.scripts_listbox.bind("<Button-3>", self.show_context_menu)

        
    def show_context_menu(self, event):
        """
        Muestra el menú contextual en las coordenadas del mouse.
        """
        self.context_menu.post(event.x_root, event.y_root)

    def new_script_popup(self):
        """
        Abre una ventana emergente.
        """
        popup = tk.Toplevel(self.root)
        popup.title("Create new Script")
        popup.geometry("300x200")

        self.new_script_form_label = tk.Label(popup, "New Script", font=("Arial", 10))

        self.entry = tk.Entry(popup, width=30)
        self.entry.pack(pady=10)
        self.entry.insert(0, "")  # Texto por defecto

        create_button = tk.Button(popup, text="Create", command=self.create_new_script_file)
        create_button.pack(pady=20)


    def open_on_editor(self, event):
        """
        Abre el archivo seleccionado en Visual Studio Code.
        """
        # Obtener el índice del archivo seleccionado
        selected_index = self.scripts_listbox.curselection()

        if selected_index:
            # Obtener el archivo de la lista usando el índice
            file_name = self.scripts_listbox.get(selected_index) + ".py"
            file_path = os.path.join(self.scripts_dir, file_name)  # Ajustar con la ruta del directorio base
            
            try:
                # Abrir el archivo con Visual Studio Code
                subprocess.Popen(["code", file_path], shell=True)
                print(f"Abriendo archivo en VS Code: {file_path}")
            except FileNotFoundError:
                print(f"No se pudo abrir el archivo: {file_path}")

    def create_new_entity_form(self, event):
        """
        Crea el formulario dinámico en el inspector para la entidad dada con un botón de cierre.
        """

        self.entity_form_notebook = ttk.Notebook(self.inspector_notebook)
        self.entity_form_notebook.place(x=0, y=800, width=self.notebook_width, height=500)

        self.form_frame = tk.Frame(self.entity_form_notebook, width=254, height=400)
        self.form_frame.place(x=0, y=5)

        # Frame para el título y el botón de cierre
        title_bar_frame = tk.Frame(self.form_frame)
        title_bar_frame.place(x=5, y=5)

        form_title_label = tk.Label(title_bar_frame, text="New Entity", font=("Arial", 11))
        form_title_label.pack(side=tk.LEFT)

        close_button = tk.Button(title_bar_frame, text="X", width=2, command=self.close_entity_form)
        close_button.pack(side=tk.LEFT, padx=5)

        name_title_label = tk.Label(self.form_frame, text="Name", font=("Arial", 9))
        name_title_label.place(x=5, y=35)

        # Textbox para mostrar el nombre de la entidad
        self.name_data_txt = tk.Text(self.form_frame, height=1, width=34, font=("Arial", 9))
        self.name_data_txt.place(x=45, y=35)

        add_entity_btn = tk.Button(self.form_frame, text="Add Entity", command=self.add_entity)
        add_entity_btn.place(x=45, y=65)  # Ubicar el botón en la esquina izquierda superior

        add_class_btn = tk.Button(self.form_frame, text="Add Class", command=self.add_class)
        add_class_btn.place(x=130, y=65)  # Ubicar el botón en la esquina izquierda superior

        self.entity_form_notebook.add(self.form_frame, text="Form")
        self.entity_form_notebook.select(self.form_frame) # Selecciona la nueva pestaña

        self.childrens.append(self.entity_form_notebook)

    def close_entity_form(self):
        """
        Cierra la pestaña del formulario de la nueva entidad.
        """
        if self.entity_form_notebook:
            self.entity_form_notebook.destroy()
            self.entity_form_notebook = None # Limpia la referencia
            # También podrías querer removerlo de self.childrens si es necesario
            if self.entity_form_notebook in self.childrens:
                self.childrens.remove(self.entity_form_notebook)
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


    def add_class(self):

        pass 
