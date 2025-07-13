from typing import List, Dict, Optional

class TasksService:
    def __init__(self, tasks_repository):
        self.tasks_repository = tasks_repository
        
    def get_completed_tasks(self) -> List:
        return self.tasks_repository.get_completed_tasks()
    
    def get_pending_tasks(self) -> List:
        return self.tasks_repository.get_pending_tasks()
    
    def get_tasks(self):
        return self.tasks_repository.get_tasks()
        
    def add_task(self, task):
        return self.tasks_repository.add_task(task)
    
    def delete_task(self, task_id: int):
        return self.tasks_repository.delete_task(task_id)