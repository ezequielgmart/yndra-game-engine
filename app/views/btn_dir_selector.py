# import tkinter as tk
from app.views.view import viewComponent


class ButtonDirSelector(viewComponent):
    
    def __init__(self, root, text, dir_selector_component):
        
        super().__init__(root)

        # Botón para seleccionar carpeta
        btn = self.tk.Button(root, text=text, command=lambda: dir_selector_component())
        btn.pack(pady=20)