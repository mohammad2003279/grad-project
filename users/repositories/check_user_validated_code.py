from abc import ABC, abstractmethod

class CheckUserValidatedCode(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> dict:
        pass

    @abstractmethod
    def delete(self, email: str) -> None:
        pass