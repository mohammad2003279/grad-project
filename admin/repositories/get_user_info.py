from abc import ABC,abstractmethod
from admin.entities.admin_entities import AdminUserEntities,AdminDoctorEntities
from utils.models import User
class ReadUsersInfoRepositories(ABC):
    @abstractmethod
    def get_by_id(self,user_id:int) -> AdminUserEntities:
        pass
    @abstractmethod
    def get_by_role(self,role:str):
        pass
    @abstractmethod
    def get_all_users_info(self)-> AdminUserEntities:
        pass