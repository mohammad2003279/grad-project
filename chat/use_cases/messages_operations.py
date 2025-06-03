from chat.repositories.message_repository import MessageRepository, MessageHistoryRepository
from chat.entities.message_entity import MessageEntity

class GetPendingMessagesUseCase:
    def __init__(self, repo: MessageRepository):
        self.repo = repo

    def execute(self,sender_id: int, receiver_id: int):
        return self.repo.get_pending_messages(sender_id, receiver_id)
    

class SaveMessagesUseCase:
    def __init__(self, repo: MessageRepository):
        self.repo = repo

    def execute(self, message: MessageEntity):
        self.repo.add(message)

class GetChatHistory:
    def __init__(self, repo: MessageHistoryRepository):
        self.repo = repo

    def execute(self, sender_id: int, receiver_id: int):
        return self.repo.get_old_messages(sender_id=sender_id, receiver_id=receiver_id)