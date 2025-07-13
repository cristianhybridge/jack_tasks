from src.views.base_view import BaseView
from tkinter import ttk

class MainView(BaseView):
    def __init__(self, master, show_view_callback):
        super().__init__(master, show_view_callback)
        self.config(bg="#3e32a8")
        
        self._create_widgets()

    def _create_widgets(self):
        ttk.Label(self,
                  text="Jack Purple Tasks App",
                  style="main_title.TLabel"
                  ).pack(pady=(50,20))
        
        ttk.Button(self, 
                   text="Ir a tareas",
                   style="main_button.TButton",
                   command=lambda: self.navigate_to("tasks")
                   ).pack(pady=10)
