from typing import List, Dict, Optional

class TasksService:
    def __init__(self, tasks_repository, users_repository):
        self.tasks_repository = tasks_repository
        self.users_repository = users_repository # Inyectamos el repositorio de users para hacer la referencia
        
        
    def get_tasks_with_username(self) -> List[Dict]:
        tasks = self.tasks_repository.get_users()

        tasks_dict = []
        
        for t in tasks:
            creator_user = self.users_repository.get_username_by_id(tasks.created_by)
            tasks_dict_copy = tasks.__dict__.copy()
            
            if creator_user:
                tasks_dict_copy['created_by'] = creator_user.username
            else:
                tasks_dict_copy['created_by'] = 'Desconocido'
                
            tasks_dict.append(tasks_dict_copy)
        
        return tasks_dict
        
    def get_tasks(self):
        return self.tasks_repository.get_users()
        
    def add_task(self, task):
        return self.tasks_repository.add_user(task)
    
    def delete_task(self, task):
        return self.tasks_repository.delete_user(task)