from abc import ABC, abstractmethod
from typing import List
from typing import Optional
class DoctorRepository(ABC):
    @abstractmethod
    def get_top_rated_doctors(self, limit: Optional[int] = None) -> List:
        pass
