class TasksService:
    def __init__(self, tasks_repository):
        self.tasks_repository = tasks_repository
        
    def get_tasks(self):
        return self.tasks_repository.get_tasks()
        
    def add_task(self, task):
        return self.tasks_repository.add_task(task)
    
    def delete_task(self, task):
        return self.tasks_repository.delete_task(task)