from models.users_entity import UserEntity
from typing import List, Dict, Optional

class UsersRepository:
    def __init__(self):
        self._users: List[UserEntity] = []
        self._next_id = 1
        
    def get_users(self) -> List[UserEntity]:
        return list(self._users)
    
    def get_username_by_id(self, user_id: int) -> Optional[UserEntity]:
        for user in self._users:
            if user.user_id == user_id:
                return user
        return None
    
    def add_user(self, user: UserEntity) -> UserEntity:
        self._users.append(user)
        return user
    
    def delete_task(self, user_id: int) -> bool:
        initial_len = len(self._users)
        self._users = [t for t in self._users if t.user_id != user_id]
        return len(self._users) < initial_len
    
    def update_task(self, user_id: int, entity_to_update: Dict) -> Optional[UserEntity]:
        for user in self._users:
            if user.user_id == user_id:
                if "username" in entity_to_update:
                    user.username = entity_to_update["username"]
                return user
        return None