import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os, subprocess, json 
from app.settings import STATE 

class AssetsNotebook:
    
    def __init__(self, root, scripts_files):

        self.root = root
        self.scripts_files = scripts_files

        # Crear el Notebook
        self.assets_tab = ttk.Notebook(self.root)
        self.assets_tab.place(x=250, y=850, width=1367, height=600)

        # Crear el Frame que contendrá los elementos
        self.scripts_frame = tk.Frame(self.assets_tab)
        self.scripts_frame.pack(fill="both", expand=True)

        # Agregar la pestaña al Notebook
        self.assets_tab.add(self.scripts_frame, text="Scripts")

        # Cargar el ícono de script
        script_icon = Image.open("data/py_icon.png")  # Cambia esta ruta por la de tu imagen
        script_icon_image_resized = script_icon.resize((40, 40))  # Redimensionar la imagen
        self.icon_photo = ImageTk.PhotoImage(script_icon_image_resized)

        # Crear lista de elementos en la pestaña
        icon_margin =20
        script_name_margin = 10

        for script in self.scripts_files:
            # Crear un Label para el ícono
            icon_label = tk.Label(self.scripts_frame, image=self.icon_photo)
            icon_label.place(x=icon_margin, y=25)

            # Crear un Label para el nombre con ajuste de texto
            script_label = tk.Label(self.scripts_frame, text=script, font=("Arial", 7), wraplength=70, justify="center")
            script_label.place(x=script_name_margin, y=70, width=70)  # Limitar el ancho del área

            # Aumentar el padding para los siguientes elementos
            icon_margin += 80
            script_name_margin += 80


        tab2 = ttk.Frame(self.assets_tab)
        tab4 = ttk.Frame(self.assets_tab)

        # create_button = tk.Button(self.scripts_frame, text="New Script", command=self.new_script_popup)
        # create_button.place(x=14, y=20)  # Ubicar el botón en la esquina derecha superior
        

        # Agregar las pestañas al Notebook
        self.assets_tab.add(self.scripts_frame, text="Scripts")
        self.assets_tab.add(tab2, text="Images")
        self.assets_tab.add(tab4, text="Sounds")