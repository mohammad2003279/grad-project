from abc import ABC,abstractmethod
from admin.entities.admin_entities import AdminRecordsEntities
class ReadTestRecordsRepositories(ABC):
    @abstractmethod
    def get_all_test_records(self) -> AdminRecordsEntities:
        pass
    @abstractmethod
    def get_records_by_userid(self,user_id:int) -> AdminRecordsEntities:
        pass
    @abstractmethod
    def get_record_by_img_id(self,img_id:int) -> AdminRecordsEntities:
        pass
        