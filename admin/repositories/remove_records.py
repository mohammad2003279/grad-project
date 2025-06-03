from abc import ABC,abstractmethod


class RemoveTestRecordsRepositories(ABC):
    @abstractmethod
    def removeRecords(self,img_id:int) -> None:
        pass