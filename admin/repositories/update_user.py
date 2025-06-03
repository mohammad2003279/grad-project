from abc import ABC,abstractmethod
from admin.entities.admin_entities import AdminDoctorEntities
from admin.entities.admin_entities import AdminUserEntities

class SuspensionUserRepositories(ABC):
    @abstractmethod
    def suspensionUser(self,user_id:int):
        pass
class AcceptionDoctorRepositories(ABC):
    @abstractmethod
    def acceptionDoctor(self,doctor_id:int):
        pass