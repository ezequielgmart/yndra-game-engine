# import tkinter as tk
from app.views.view import viewComponent
from tkinter import filedialog


class DirSelector(viewComponent):

    def __init__(self, root):
        super().__init__(root)

        # Abrir diálogo para seleccionar carpeta
        self.dir_selected = filedialog.askdirectory(title="select a folder")  # Ahora es un atributo de la instancia
        
        
class ButtonDirSelector(viewComponent):
    
    def __init__(self, root, text, dir_selector_component):
        
        super().__init__(root)

        # Botón para seleccionar carpeta
        btn = self.tk.Button(root, text=text, command=lambda: dir_selector_component(root))
        btn.pack(pady=20)        
        