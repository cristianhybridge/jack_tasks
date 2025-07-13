from src.models.tasks_entity import TaskEntity
from typing import List, Dict, Optional
import datetime

class TasksRepository:
    def __init__(self):
        self._tasks: List[TaskEntity] = [] # Lista para almnacenar tasks en memoria

    # def get_tasks(self) -> List[TaskEntity]:
    #     return list(self._tasks)
    
    def get_completed_tasks(self) -> List[TaskEntity]:
        return list(filter(lambda task: 
                           task.required_date > datetime.datetime.now() or task.marked_as_completed
                           ,self._tasks))

    def get_pending_tasks(self) -> List[TaskEntity]:
        return list(filter(lambda task: task.marked_as_completed == False and task.required_date < datetime.datetime.now(),
                           self._tasks))
    
    def add_task(self, task: TaskEntity) -> TaskEntity:
        self._tasks.append(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        initial_len = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.task_id != task_id]
        return len(self._tasks) < initial_len # Retorna True si se eliminó algo
    
    def mark_as_completed(self, task_id: int):
        if task_id in [t.task_id for t in self._tasks]:
            task = [t for t in self._tasks if t.task_id == task_id][0]
            task.marked_as_completed = True
        