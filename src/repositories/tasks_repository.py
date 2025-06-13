from typing import List, Dict
from models.tasks_entity import TaskEntity

class TasksRepository:
    def __init__(self):
        self._tasks: List[Dict] = [] # Lista para almnacenar tasks en memoria
        self._next_id = 1 # Contador para asignar IDs incrementales

    def get_tasks(self) -> List[Dict]: # Definir el tipado que se retornara
        return list(self._tasks) # Retorna una copia para evitar modificaciones directas

    def add_task(self, task: Dict) -> Dict:
        """Añade una nueva tarea y le asigna un ID simple."""
        task_id = str(self._next_id) # Asigna el ID como un numero en string
        self._next_id += 1 # Incrementa el contador
        task_with_id = {**task, "id": task_id} # Añade el ID
        self._tasks.append(task_with_id)
        return task_with_id

    def delete_task(self, task_id: str) -> bool:
        """Elimina una tarea por su ID."""
        initial_len = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.get("id") != task_id]
        return len(self._tasks) < initial_len # Retorna True si se eliminó algo

    def update_task(self, task_id: str, new_data: Dict) -> Dict | None:
        """Actualiza una tarea existente."""
        for i, task in enumerate(self._tasks):
            if task.get("id") == task_id:
                self._tasks[i].update(new_data)
                return self._tasks[i]
        return None # Tarea no encontrada