import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
# from app.settings import STATE 

class MainCanvas:
    

    def __init__(self, root, project_file_data):

        self.root = root

        self.project_file_data = project_file_data

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
