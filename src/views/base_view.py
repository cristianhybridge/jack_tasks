import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import ttk
from app_styles import configure_styles

class BaseView(ABC, tk.Frame):
    """
    Clase base para todas las vistas de la aplicacion
    Sin embargo, como estoy haciendo una app minimalista, solo estoy haciendo una herencia abstracta
    a traves de una interfaz (ABC)
    """
    def __init__(self, master, show_view_callback):
        super().__init__(master)
        self.master = master # La ventana principal (App)
        self.show_view_callback = show_view_callback # La función para cambiar de vista

    @abstractmethod
    def _create_widgets(self):
        pass
    @abstractmethod
    def _build_ui(self):
        pass