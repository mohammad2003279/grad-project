from abc import ABC,abstractmethod
from users.entities.user_entites import UserRecordsEntities
class ReadTestRecordsRepositories(ABC):
    @abstractmethod
    def get_records_by_userid(self,user_id:int) -> UserRecordsEntities:
        pass