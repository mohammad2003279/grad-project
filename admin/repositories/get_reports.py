from abc import ABC,abstractmethod
from typing import List,Dict,Any

class GetAllReportsRepositories(ABC):
    @abstractmethod
    def get_all_reports(self) -> List[Dict[str, Any]]:
        pass
    @abstractmethod
    def get_all_reports_by_status(self,status:str) -> List[Dict[str, Any]]:
        pass