from abc import ABC, abstractmethod
from chat.entities.message_entity import MessageEntity
from datetime import timedelta

class MessageRepository(ABC):
    @abstractmethod
    def get_pending_messages(self,sender_id: int, receiver_id: int) -> list[MessageEntity]:
        pass

    def add(self, message: MessageEntity) -> None:
        pass


class MessageHistoryRepository(ABC):
    @abstractmethod
    def get_old_messages(self, sender_id: int, receiver_id: int, back_in_time: timedelta = timedelta(hours=24)) -> dict:
        pass