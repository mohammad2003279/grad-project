from abc import ABC, abstractmethod
from users.entities.user_entites import UserEntity

class DoctorInformationRepository(ABC):
    @abstractmethod
    def get_by_email(self, doctor_id: int) -> UserEntity:
        pass

    @abstractmethod
    def get_acceptation_result(self, doctor_id: int) -> bool:
        pass

    @abstractmethod
    def get_doctor_bio(self, doctor_id: int) -> str:
        pass

    @abstractmethod
    def rate_doctor(self, doctor_id: int, rate: int) -> None:
        pass
    
class DoctorsRepository(ABC):
    @abstractmethod
    def get_top_rated_doctors(self, limit: int = 5) -> list:
        pass
