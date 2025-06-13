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
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())) # Genera un ID por cada task nuevo
    completion_date: datetime | None = None
    is_active: bool = True
    
    def mark_as_completed(self):
        self.is_active = False
        self.completion_date = datetime.now()
        
    @property
    def is_completed(self):
        return self.completion_date is not None