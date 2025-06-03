from abc import ABC, abstractmethod
from scan.entities.test_record_entity import TestRecordEntity

class ScanImageRepository(ABC):

    @abstractmethod
    def add(self, request: TestRecordEntity):
        pass

    def update(self, user_id: int):
        pass