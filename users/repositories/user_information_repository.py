from abc import ABC, abstractmethod
from users.entities.user_entites import UserEntity

class UserInformationRepository(ABC):
    @abstractmethod
    def add(self, user_id: int, path: str):
        pass

    @abstractmethod
    def get_profile_pic(self, user_id: int)-> str:
        pass

    @abstractmethod
    def get_basic_info(self, user_id: int)-> UserEntity:
        pass