from abc import ABC, abstractmethod
from auth.entities.verification_request import VerificationRequest
from users.schemas.create_account_schema import CreateAccountSchema

class CreateAccountRequestRepository(ABC):
    @abstractmethod
    def add(self, cam: CreateAccountSchema): #cam stands for create account model
        pass

class CreateDoctorAccountRepository(ABC):
    @abstractmethod
    def add(self, email: str):
        pass
