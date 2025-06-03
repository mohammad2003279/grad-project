from abc import ABC,abstractmethod
from admin.entities.admin_entities import AdminDoctorEntities


class GetDoctorsByAcception(ABC):
    @abstractmethod
    def get_doctors_by_acception(self,acception:bool) -> AdminDoctorEntities:
        pass