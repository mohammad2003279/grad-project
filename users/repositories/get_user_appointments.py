from abc import ABC, abstractmethod
from typing import List
from users.entities.user_entites import AppointmentEntity

class AppointmentPatientRepo(ABC):
    @abstractmethod
    def get_all_appointments(self, user_id: int) -> List[AppointmentEntity]:
        pass
    def cancel_appointments(self,appointment_id:int,user_id:int)->None:
        pass