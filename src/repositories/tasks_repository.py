from src.models.tasks_entity import TaskEntity
from typing import List, Dict, Optional
import datetime

class TasksRepository:
    def __init__(self):
        self._tasks: List[TaskEntity] = [] # Lista para almnacenar tasks en memoria

    def get_tasks(self) -> List[TaskEntity]:
        return list(self._tasks)
    
    def get_completed_tasks(self) -> List[TaskEntity]:
        return list(filter(lambda task: task.completion_date < datetime.datetime.now(),
                           self._tasks))
    
    def get_pending_tasks(self) -> List[TaskEntity]:
        return list(filter(lambda task: task.completion_date >= datetime.datetime.now(), self._tasks))
    
    def add_task(self, task: TaskEntity) -> TaskEntity:
        self._tasks.append(task)
        return task

    def update_task(self, task_id: str, entity_to_update: Dict) -> Optional[TaskEntity]:
        for task in self._tasks:
            if task.task_id == task_id: # Accede al atributo .task_id del objeto TaskEntity
                if "title" in entity_to_update:
                    task.title = entity_to_update["title"]
                if "priority" in entity_to_update:
                    task.priority = entity_to_update["priority"]
                if "completion_date" in entity_to_update:
                    task.completion_date = entity_to_update["completion_date"]
                if "is_active" in entity_to_update:
                    task.is_active = entity_to_update["is_active"]
                return task
        return None