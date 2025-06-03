from abc import ABC, abstractmethod
from auth.entities.user_entities import CheckUserRequest, CheckUserExistRequest

class CheckUserRequestRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> bool:
        pass


class CheckUserExistRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> CheckUserExistRequest:
        pass