from views.base_view import BaseView
import tkinter as tk
from tkinter import ttk

class OptionsView(BaseView):
    def __init__(self, master, show_view_callback, current_username):
        super().__init__(master, show_view_callback, current_username)
        self.config(bg="#e0e0ff") # Otro color para esta vista


        self.selected_color = tk.StringVar(value="#000000") # Inicializar con negro
        self.red_value = tk.IntVar(value=0)   # Valor inicial para Rojo
        self.green_value = tk.IntVar(value=0) # Valor inicial para Verde
        self.blue_value = tk.IntVar(value=0)  # Valor inicial para Azul
        
        self._create_widgets()

    def _create_widgets(self):
        welcome_message = f"Bienvenido, {self.current_username}"
        
        ttk.Label(self,
                  text=f"{welcome_message}",
                  style="main_title.TLabel"
                  ).pack(pady=50)

        ttk.Button(self,
                   text="Volver",
                   style="main_button.TButton",
                   command=lambda: self.navigate_to("main")
                   ).pack(pady=10)