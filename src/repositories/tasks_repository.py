from models.tasks_entity import TaskEntity
from typing import List, Dict, Optional

class TasksRepository:
    def __init__(self):
        self._tasks: List[TaskEntity] = [] # Lista para almnacenar tasks en memoria
        self._next_id = 1 # Contador para asignar IDs incrementales

    def get_tasks(self) -> List[TaskEntity]:
        return list(self._tasks) # Retorna una copia para evitar modificaciones directas
    
    def get_completed_tasks(self) -> List[TaskEntity]:
        return list(filter(lambda task: not task.is_active, self._tasks))
    
    def get_pending_tasks(self) -> List[TaskEntity]:
        return list(filter(lambda task: task.is_active, self._tasks))
    
    def add_task(self, task: TaskEntity) -> TaskEntity:
        self._tasks.append(task)
        return task

    def delete_task(self, task_id: str) -> bool:
        initial_len = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.task_id != task_id]
        return len(self._tasks) < initial_len # Retorna True si se eliminó algo

    def update_task(self, task_id: str, entity_to_update: Dict) -> Optional[TaskEntity]:
        for task in self._tasks: # Iteramos sobre los objetos TaskEntity
            if task.task_id == task_id: # <--- Accede al atributo .task_id del objeto TaskEntity
                # Actualiza los atributos del objeto TaskEntity si vienen en new_data
                if "title" in entity_to_update:
                    task.title = entity_to_update["title"]
                if "priority" in entity_to_update:
                    task.priority = entity_to_update["priority"]
                if "completion_date" in entity_to_update:
                    task.completion_date = entity_to_update["completion_date"]
                if "is_active" in entity_to_update:
                    task.is_active = entity_to_update["is_active"]
                # Puedes añadir más campos aquí si los agregas a tu entidad TaskEntity
                return task # Retorna el objeto TaskEntity actualizado
        return None # Tarea no encontrada