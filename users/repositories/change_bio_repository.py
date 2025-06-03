from abc import ABC, abstractmethod

class ChangeBioRepository(ABC):

    @abstractmethod
    def get_by_email(self, user_id: int):
        pass

    @abstractmethod
    def update(self, bio: str, user_id: int):
        pass