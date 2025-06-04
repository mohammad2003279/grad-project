from abc import ABC, abstractmethod
from typing import List

class DoctorRepository(ABC):
    @abstractmethod
    def get_top_rated_doctors(self, limit: int = 5) -> List:
        pass