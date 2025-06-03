from abc import ABC, abstractmethod
from users.entities.user_entites import UserEntity

class ChangeInfoRepository(ABC):
    @abstractmethod
    def update(self, update_info_entity: UserEntity):
        pass

class ChangePasswordRepository(ABC):
    @abstractmethod
    def get_by_email(self, user_id: int) -> UserEntity:
        pass

    @abstractmethod
    def update(self, udpate_password_entity: UserEntity) -> None:
        pass

class ChangeForgetPasswordRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> dict:
        pass


    @abstractmethod
    def delete(self, email: str) -> None:
        pass
    @abstractmethod
    def update(self, udpate_password_entity: UserEntity) -> None:
        pass