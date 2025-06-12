from views.base_view import BaseView
import tkinter as tk
from tkinter import ttk

class TaskManagementView(BaseView):
    def __init__(self, master, show_view_callback, current_username):
        super().__init__(master, show_view_callback, current_username)
        self.config(bg="#e0ffe0") # Un colorcito diferente para diferenciar

    def _create_widgets(self):
        ttk.Label(self,
                  text="Administrar tareas",
                  style="main_title.TLabel"
                  ).pack(pady=50)

        ttk.Button(self,
                   text="Volver",
                   style="main_button.TButton",
                   command=lambda: self.navigate_to("main")
                   ).pack(pady=10)

        ttk.Button(self, text="Ajustes",
                   style="secondary_button.TButton",
                   command=lambda: self.navigate_to("options")
                   ).pack(pady=10)