from views.base_view import BaseView
from tkinter import ttk

class MainView(BaseView):
    def __init__(self, master, show_view_callback, current_username):
        super().__init__(master, show_view_callback, current_username)
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

        ttk.Button(self, text="Ajustes",
                   style="secondary_button.TButton",
                   command=lambda: self.navigate_to("options")
                   ).pack(pady=10)

    def _setup_layout(self):
        # En el diseño minimalista con .pack(), no siempre necesitas un setup_layout complejo.
        # Los widgets se empaquetan en orden.
        pass