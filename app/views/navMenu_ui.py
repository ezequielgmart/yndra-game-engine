import tkinter as tk
from app.views.dir_selector import DirSelector
import os, subprocess, json 
from app.settings import STATE 

class NavMenu:

    def __init__(self, root):
        self.root = root


        self.menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.select_project)
        file_menu.add_separator()  # Separador entre opciones
        file_menu.add_command(label="Exit", command=self.root.quit)

        execute_menu = tk.Menu(self.menu_bar, tearoff=0)
        execute_menu.add_command(label="Play Game", command=self.run_script)

        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.menu_bar.add_cascade(label="Run", menu=execute_menu)

        self.root.config(menu=self.menu_bar)

        
    
    def select_project(self, *args): 
        selected_path = DirSelector(self.root).dir_selected
        if selected_path:
            STATE.content['project_path'] = selected_path
            self.root.title(selected_path)
            STATE.add_project(selected_path)

    def run_script(self):

        try:
            subprocess.Popen(["python", STATE.content['run_file']])
            print("Script ejecutado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Hubo un error al ejecutar el script: {e}")
        except FileNotFoundError:
            print("El archivo especificado no existe.")