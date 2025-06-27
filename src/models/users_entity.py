import uuid
from dataclasses import dataclass, field

@dataclass
class UserEntity:
    username: str
    user_id: int