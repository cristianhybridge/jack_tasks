from typing import List, Dict, Optional

class UsersService:
    def __init__(self, users_repository):
        self.users_repository = users_repository # Inyectamos el repositorio de users para hacer la referencia


    def get_users(self):
        return self.users_repository.get_users()
    
    def get_username_by_id(self, id: int):
        return self.users_repository.get_username_by_id(id)



    def add_user(self, task):
        return self.users_repository.add_user(task)

    def delete_user(self, task):
        return self.users_repository.delete_user(task)