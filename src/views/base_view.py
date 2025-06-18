import tkinter as tk
from tkinter import ttk
from app_styles import configure_styles

class BaseView(tk.Frame):
    """
    Clase base para todas las vistas (pantallas) de la aplicación.
    Provee funcionalidad común como el acceso al controlador de vistas.
    """
    def __init__(self, master, show_view_callback, current_username):
        super().__init__(master)
        self.master = master # La ventana principal (App)
        self.show_view_callback = show_view_callback # La función para cambiar de vista
        self.current_username = current_username

        self._setup_layout()

    def _create_widgets(self):
        """
        Método a sobrescribir por las clases hijas para crear sus widgets.
        """
        pass # Implementación vacía, cada vista la llenará

    def _setup_layout(self):
        """
        Método a sobrescribir por las clases hijas para configurar su layout.
        """
        pass # Implementación vacía, cada vista la llenará

    def navigate_to(self, view_name: str):
        """
        Método de conveniencia para navegar a otra vista.
        """
        self.show_view_callback(view_name)