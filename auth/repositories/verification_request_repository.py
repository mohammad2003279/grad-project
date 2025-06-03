from abc import ABC, abstractmethod
from auth.entities.verification_request import VerificationRequest

class VerificationRequestRepository(ABC):
    @abstractmethod
    def add(self, request: VerificationRequest) -> None:
        pass 
    
    @abstractmethod
    def get_by_email(self, email: str) -> dict:
        pass

    @abstractmethod
    def delete(self, email: str) -> None:
        pass

    @abstractmethod
    def update(self, email: str) -> None:
        pass
    @abstractmethod
    def check_exist(self, email: str) -> bool:
        pass