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
    # En este caso como no estamos usando SQL, puse un uuid para que no se repitiera
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())) # Genera un ID por cada task nuevo
    completion_date: datetime | None = None
    
    # Dar formato sencillo para completion_date
    @property
    def formatted_completion_date(self) -> str:
        if self.completion_date:
            return self.completion_date.strftime('%Y-%m-%d %H:%M')
        return 'N/A' # Default para robustez en caso de error
    