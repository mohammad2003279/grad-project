from auth.entities.user_entities import CheckUserExistRequest
from abc import ABC, abstractmethod
from datetime import datetime
from auth.entities.token_entity import RefreshTokenEntity

class RefreshTokenRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> CheckUserExistRequest:
        pass

    @abstractmethod
    def add(self, token: str, expires_at: datetime, user_id: int):
        pass

    @abstractmethod
    def get_by_token(self, token: str) -> RefreshTokenEntity:
        pass

    @abstractmethod
    def delete(self, token: str):
        pass

    @abstractmethod
    def update(self, old_token: str, new_token: str):
        pass