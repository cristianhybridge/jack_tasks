from dataclasses import dataclass, field
from datetime import datetime
# Libreria para generar IDS unicos
import uuid 

@dataclass
class TaskEntity:
    # Campos sin valor por defecto
    title: str
    priority: str
    
    # Campos con valor por defecto
    
    # En este caso como no estamos usando SQL, tuve que investigar e ingenierlas para poder usar database en memoria
    
    _next_id: int = 0 # Esto es para que el ID sea unico y se vaya incrementando automaticamente
    
    # No permitir que se inicialice automaticamente
    task_id: int = field(init=False, hash=False)
    
    required_date: datetime | None = None
    
    # Metodo para dar formato sencillo al required_date
    @property
    def formatted_completion_date(self) -> str:
        if self.required_date:
            return self.required_date.strftime('%Y-%m-%d %H:%M')
        return 'N/A' # Default para robustez en caso de error
    
    # El post init sirve como una continuacion del constructor o un segundo paso
    def __post_init__(self):
        self.task_id = TaskEntity._next_id
        TaskEntity._next_id += 1
    