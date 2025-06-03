from abc import ABC, abstractmethod

class VerificationRequestAccepted(ABC):
    @abstractmethod
    def add(self, email: str):
        pass