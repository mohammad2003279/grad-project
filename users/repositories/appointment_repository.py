from abc import ABC, abstractmethod
from typing import List
from users.entities.user_entites import AppointmentEntity
#I stand for Interface
class IAppointmentRepository(ABC):
    @abstractmethod
    def create_appointment(self, appointment: AppointmentEntity) -> AppointmentEntity:
        pass

    @abstractmethod
    def get_all_appointments(self, doctor_id: int) -> List[AppointmentEntity]:
        pass
    @abstractmethod
    def accept_appointment(self, appointment_id: int,user_id:int) -> AppointmentEntity:
        pass
