import tkinter as tk

from app_styles import configure_styles
from models.users_entity import UserEntity
from repositories.users_repository import UsersRepository
from views.main_view import MainView
from views.tasks_view import TaskManagementView
from views.options_view import OptionsView

from repositories.tasks_repository import TasksRepository
from services.tasks_service import TasksService
from services.users_service import UsersService

class App(tk.Tk):
    # Clase principal
    def __init__(self):
        super().__init__()
        self.title("Jack Purple Tasks App")
        self.geometry("1280x800") # Tamano de la ventana
        
        configure_styles() # Funcion para configurar estilos
        
        self.tasks_repository = TasksRepository() # Instancia de la clase TasksRepository
        self.users_repository = UsersRepository() # Instancia de la clase UsersRepository

        # Instancia del servicio, recibe los repositorios
        self.tasks_service = (
            TasksService(self.tasks_repository, self.users_repository))
        self.users_service = (
            UsersService(self.users_repository)
        )
        
        # ------------------------------- Hardcodeado para pruebas
        self.current_username = "None" # Se inicializa variable
        self._insert_user_test() # Aqui se sobreescribe la variable
        # -------------------------------
        self._current_view = None
        self._views = {} # Diccionario para guardar instancias de las vistas

        self._create_views()
        self.show_view("main") # Vista principal al iniciar aplicacion
        
        # ------------------------------- Hardcodeado para pruebas
    def _insert_user_test(self):
        self.users_repository.add_user(UserEntity("admin", 1))
        
        # test_username = self.users_service.get_user_by_id(1)
        
        # self.current_username = test_username.username
        self.current_username = (self.users_service.get_username_by_id(1)).username
        print(f"DEBUG: Current username: {self.current_username}")
    def _create_views(self):
        """Crea instancias de todas las vistas."""
        self._views["main"] = MainView(self, self.show_view, self.current_username)
        self._views["tasks"] = TaskManagementView(self, 
                                                  self.show_view, 
                                                  self.current_username,
                                                  self.tasks_service,
                                                  self.users_service)
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