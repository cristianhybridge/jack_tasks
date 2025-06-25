import tkinter as tk

from app_styles import configure_styles
from views.main_view import MainView
from views.tasks_view import TaskManagementView
from views.options_view import OptionsView

from repositories.tasks_repository import TasksRepository
from services.tasks_service import TasksService

class App(tk.Tk):
    # Clase principal
    def __init__(self):
        super().__init__()
        self.title("Jack Purple Tasks App")
        self.geometry("1280x800") # Tamano de la ventana
        
        configure_styles() # Funcion para configurar estilos
        
        self.tasks_repository = TasksRepository() # Instancia de la clase TasksRepository
        self.tasks_service = TasksService(self.tasks_repository) # Instancia del servicio, recibe el repositorio
        
        # -------------------------------
        self.current_username = "Cris"
        # -------------------------------
        self._current_view = None
        self._views = {} # Diccionario para guardar instancias de las vistas

        self._create_views()
        self.show_view("main") # Vista principal al iniciar aplicacion
    def _create_views(self):
        """Crea instancias de todas las vistas."""
        self._views["main"] = MainView(self, self.show_view, self.current_username)
        self._views["tasks"] = TaskManagementView(self, 
                                                  self.show_view, 
                                                  self.current_username,
                                                  self.tasks_service)
        self._views["options"] = OptionsView(self, self.show_view, self.current_username)

        # Empaqueta todas las vistas para que estén listas para ser mostradas
        for view_name, view_instance in self._views.items():
            view_instance.pack(fill="both", expand=True)
            view_instance.pack_forget() # Las oculta inicialmente

    def show_view(self, name: str):
        """
        Muestra la vista especificada por su nombre y oculta la actual.
        """
        if self._current_view:
            self._current_view.pack_forget() # Oculta la vista actual

        view_to_show = self._views.get(name)
        if view_to_show:
            view_to_show.pack(fill="both", expand=True)
            self._current_view = view_to_show
            print(f"Cambiando a la vista: {name}")
        else:
            print(f"Error: Vista '{name}' no encontrada.")

if __name__ == "__main__":
    app = App()
    app.mainloop()