import tkinter as tk

import os, subprocess, json 
from app.settings import STATE 

from app.views.navMenu_ui import NavMenu
from app.views.mainCanvas_ui import MainCanvas
from app.views.assetsNotebook_ui import AssetsNotebook
from app.views.inspectorNotebook_ui import InspectorNotebook
from app.views.resourcesNotebook_ui import ResourcesNotebook



class WindowsApp:

    def __init__(self):
        # Crear la ventana principal
        self.root = tk.Tk()
        
        # Tamaño de la ventana (ancho x alto)
        self.root.geometry("1920x1080")  


        self.root.state("zoomed") 

        # Cargar los elementos del archivo JSON
        
        self.levels_file = self.read_json_file(STATE.content['project_path'] + "\\assets\\levels\\initial_level.json")

        self.scripts_dir = STATE.content['project_path'] + "\\assets\\scripts"
        # obtener todos lso archivos de scripts
        self.scripts_files = self.get_scripts_files(self.scripts_dir)
        
        self.entities_classes_json = self.read_json_file(STATE.content['project_path'] + "\\assets\\data\\entity_classes.json")


        self.project_file_data = self.read_json_file(STATE.content['project_path'] + "\\project.json")

        self.project_file_data = self.project_file_data["project"]

          
        # Cargar las entidades en el Listbox
        self.entities_classes = self.entities_classes_json['collection_entities'] # Acceder a las entidades

        if STATE.content['project_path'] == "":
            self.root.title("IKARUS ENGINE")
        else: 
            self.root.title(f"IKARUS ENGINE | {STATE.content['project_name']} | {STATE.content['project_path']}")

        ############### MAIN BAR MENU ############################################
        self.menu_bar = NavMenu(self.root)

        ############### PLAY GAME BUTTON #########################################
        run_button = tk.Button(self.root, text="Play Game", command=self.run_script)
        run_button.place(x=850, y=5)  # Ubicar el botón en la esquina izquierda superior

        ############### MAIN CANVAS ##############################################
        self.level_designer_tab = MainCanvas(self.root, self.project_file_data)


        ##### ASSETS TABS ########################################################
        self.assets_tab = AssetsNotebook(self.root, self.scripts_files)
   

        ##### INSPECTOR TABS #####################################################
        self.hierarchy = ResourcesNotebook(self.root, self.levels_file, self.entities_classes, self.scripts_dir)
        
        ####### ENTITIES CLASSES ########## 
        
        ##### INSPECTOR # # # # # # # 
        self.inspector_notebook = InspectorNotebook(self.root, self.levels_file, self.scripts_dir)

        ####### SCRIPTS ########## 
        
        # self.listbox = tk.Listbox(self.root, width=40, height=16)
        # self.listbox.place(x=1, y=720)

        # # Cargar las entidades en el Listbox
       
        # for file in self.scripts_files:
        #     # entity_name = entity['entity_name']
        #     self.listbox.insert(tk.END, f"{file}")

        # # Asociar evento para mostrar el id de la entidad seleccionada
        # self.listbox.bind("<<ListboxSelect>>", self.open_on_editor)

        # Etiqueta para mostrar los detalles de la entidad seleccionada

        #

        # Ejecución del bucle principal de la ventana
        self.root.mainloop()

    def open_with_vscode_option(self, event):
        """
        Abre el archivo seleccionado en Visual Studio Code.
        """
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_file = self.listbox.get(selected_index)
            file_path = os.path.join(self.scripts_dir, selected_file)
            try:
                os.system(f"code {file_path}")  # Abrir con VS Code
                print(f"Abrir archivo: {file_path}")
            except Exception as e:
                print(f"No se pudo abrir el archivo: {e}")
        else:
            print("No se seleccionó ningún archivo.")

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


    def display_entity_components(self, entity_data):
        """
        Crea el formulario dinámico en el inspector para los componentes de la entidad o clase.
        """
        if len(self.inspector_widgets) > 0:

            self.clear_inspector()  # Limpiar el inspector antes de mostrar nuevos widgets
        # self.create_inspector_form(entity_data)
        
        self.create_inspector_form(entity_data)


    def clear_inspector(self):
        """
        Borra los widgets anteriores del inspector.
        """
        for widget in self.inspector_widgets:
            widget.destroy()
        self.inspector_widgets = []
        """Elimina el label dentro del frame."""
    # for widget in frame.winfo_children():
    #     if isinstance(widget, tk.Label):
    #         widget.destroy()
    #         break  # Detener después de eliminar el primer Label



    def create_inspector_form(self, entity):
        """
        Crea el formulario dinámico en el inspector para la entidad dada.
        """
        x_location = 10
        y_location = 10

        # Label para el nombre de la entidad
        name_label = tk.Label(self.inspector_tab, text="Entity Name")
        name_label.place(x=x_location, y=y_location)  # Posicionamos el Label


        self.inspector_widgets.append(name_label)

        # Textbox para mostrar el nombre de la entidad
        name_data_txt = tk.Text(self.inspector_tab, height=1, width=20)
        name_data_txt.place(x=x_location, y=(y_location + 25))
        name_data_txt.insert(tk.END, entity["entity_name"])  # Insertamos el texto inicial
        name_data_txt.config(state=tk.DISABLED)  # Hacemos el textbox de solo lectura

        self.inspector_widgets.append(name_data_txt)
        
        # Botón para agregar un componente
        add_component_btn = tk.Button(self.inspector_tab, text="Add Component", command=self.new_script_popup)
        add_component_btn.place(x=x_location, y=(y_location + 45))  # Posicionamos dinámicamente después de todos los elementos
        self.inspector_widgets.append(add_component_btn)

        # Actualizamos la posición vertical
        y_location += 85  # Espaciamos después del nombre de la entidad
        
        for component in entity["components"]:

            if component["type"] == "Position":

                add_component_btn = tk.Button(self.inspector_tab, text="Position", width=40, command=self.position_btn_component_action)
                add_component_btn.place(x=x_location, y=(y_location))  # Posicionamos dinámicamente después de todos los elementos
                self.inspector_widgets.append(add_component_btn)

                
                y_location += 30

            if component["type"] == "Render":

                add_component_btn = tk.Button(self.inspector_tab, text="Render", width=40, command=self.position_btn_component_action)
                add_component_btn.place(x=x_location, y=(y_location))  # Posicionamos dinámicamente después de todos los elementos
                self.inspector_widgets.append(add_component_btn)

                
                y_location += 30

            if component["type"] == "behaviour":

                add_component_btn = tk.Button(self.inspector_tab, text="Behaviour", width=40, command=self.position_btn_component_action)
                add_component_btn.place(x=x_location, y=(y_location))  # Posicionamos dinámicamente después de todos los elementos
                self.inspector_widgets.append(add_component_btn)

                
                y_location += 30

    def position_btn_component_action(self):

        if len(self.inspector_widgets) > 0:

            self.clear_inspector()  # Limpiar el inspector antes de mostrar nuevos widgets
        # self.create_inspector_form(entity_data)
        
        
        # self.entity_on_use.clear()

        print(self.entity_on_use)


        """
        {
            'entity_id': 5, 
            'entity_name': 'bigrock4', 
            'components': [
                {'type': 'Position', 'data': {'x': 600, 'y': 400, 'rotation':0, 'scale':0}},
                {'type': 'Render', 'data': {'sprites': 'C:\\Users\\jerem\\Desktop\\asteroids\\projects\\asteroids_ECS\\assets\\sprites\\bigrock.png'}}, 
                {'type': 'behaviour', 'data': {'scripts': [
                    {
                        'path':'C:\\Users\\jerem\\Desktop\\asteroids\\projects\\asteroids_ECS\\assets\\scripts\\BigRockMovement.py', 
                        'module': 'BigRockMovement'
                    }
                ]
                }}]}
        """

    
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

    # def select_project(self, *args): 
    #     selected_path = DirSelector(self.root).dir_selected
    #     if selected_path:
    #         STATE.content['project_path'] = selected_path
    #         self.root.title(selected_path)
    #         STATE.add_project(selected_path)

    def run_script(self):
        
        script_directory = STATE.content['project_path']


        run_file = os.path.join(STATE.content['project_path'], "game.py")

        try:
            # Obtener el directorio del archivo a ejecutar
            
            # Ejecutar el script desde su directorio
            subprocess.Popen(["python", run_file], cwd=script_directory)
            print("Script ejecutado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Hubo un error al ejecutar el script: {e}")
        except FileNotFoundError:
            print("El archivo especificado no existe.")

    def read_json_file(self, json_file):
        with open(json_file, "r") as f:
            data = json.load(f)
        return data


    def get_dir_files(self,path):
        try:
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            return files
        except FileNotFoundError:
            print("Dir not found.")
            return []
        
    def show_context_menu(self, event):
        """
        Muestra el menú contextual en las coordenadas del mouse.
        """
        self.context_menu.post(event.x_root, event.y_root)

    def get_scripts_files(self, path):

            try:

                files = []  # Crear una lista vacía para almacenar los archivos

                for f in os.listdir(path):  # Iterar sobre todos los elementos en el directorio

                    full_path = os.path.join(path, f)  # Obtener la ruta completa del elemento

                    if os.path.isfile(full_path):  # Verificar si es un archivo

                        if f == "__init__.py":
                            pass
                        else:
                            files.append(f)  # Agregar el archivo a la lista



                return files
            except FileNotFoundError:
                print("Dir not found.")
                return []