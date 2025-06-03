from abc import ABC, abstractmethod

class UserReportRepository(ABC):
    @abstractmethod
    def report_user(self,user_id:int,user_reported:int,description:str,report_type:str)-> None:
        pass