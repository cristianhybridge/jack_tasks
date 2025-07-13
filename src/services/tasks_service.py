from typing import List, Dict, Optional

class TasksService:
    def __init__(self, tasks_repository):
        self.tasks_repository = tasks_repository
        
        
    def get_tasks_with_username(self) -> List[Dict]:
        tasks = self.tasks_repository.get_users()

        tasks_dict = []
        
        for t in tasks:
            tasks_dict_copy = tasks.__dict__.copy()
            
            tasks_dict.append(tasks_dict_copy)
        
        return tasks_dict
        
    def get_completed_tasks(self) -> List:
        return self.tasks_repository.get_completed_tasks()
    
    def get_pending_tasks(self) -> List:
        return self.tasks_repository.get_pending_tasks()
    
    def get_tasks(self):
        return self.tasks_repository.get_tasks()
        
    def add_task(self, task):
        return self.tasks_repository.add_task(task)
    
    def delete_task(self, task):
        return self.tasks_repository.delete_user(task)