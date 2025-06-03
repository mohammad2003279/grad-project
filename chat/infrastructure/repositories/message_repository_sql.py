# chat/infrastructure/message_repository_sql.py
from chat.repositories.message_repository import MessageRepository, MessageHistoryRepository
from sqlalchemy.orm import Session
from utils.models import Messages
from chat.entities.message_entity import MessageEntity
from chat.schemas.message_schema import MessageSchema
from datetime import datetime, UTC
import redis
import json

class MessageRepositorySQL(MessageRepository):
    def __init__(self, session: Session):
        self.session = session
        self.redis_server = redis.Redis(host="localhost", port=6379, db=0)

    def get_pending_messages(self, sender_id: int, receiver_id: int):
        messages = self.session.query(Messages).filter(
            Messages.receiver_id == receiver_id,
            Messages.sender_id == sender_id,
            Messages.status == 'pending'
        ).all()

        if not messages:
            return []

        messages_entities: list[MessageEntity] = []
        for i in messages:
            i.delivered_at = datetime.utcnow()  # type: ignore
            schema = MessageSchema(
                sender_id=i.sender_id,  # type: ignore
                receiver_id=i.receiver_id,  # type: ignore
                content=i.content,  # type: ignore
                sent_at=i.sent_at,  # type: ignore
                delivered_at=i.delivered_at,  # type: ignore
                status=i.status  # type: ignore
            )
            i.status = 'sent'  # type: ignore
            messages_entities.append(MessageEntity(schema))
            self.session.commit()
            self.session.refresh(i)
        return messages_entities

    def add(self, message: MessageEntity):
        msg_dict = {
            "sender_id": message.sender_id,
            "receiver_id": message.receiver_id,
            "content": message.content,
            "sent_at": str(message.sent_at),
            "delivered_at": str(message.delivered_at),
            "status": message.status
        }
        msg_json = json.dumps(msg_dict)
        self.redis_server.lpush("pending_to_save", msg_json)


class MessageHistoryRepositorySQL(MessageHistoryRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_old_messages(self, sender_id, receiver_id, back_in_time=None):
        a_to_b = self.session.query(Messages).filter(
            Messages.sender_id == sender_id,
            Messages.receiver_id == receiver_id
        )
        b_to_a = self.session.query(Messages).filter(
            Messages.sender_id == receiver_id,
            Messages.receiver_id == sender_id
        )

        history_a_to_b = [
            MessageEntity(MessageSchema(
                sender_id=msg.sender_id,
                receiver_id=msg.receiver_id,
                content=msg.content,
                sent_at=msg.sent_at,
                delivered_at=msg.delivered_at,
                status=msg.status
            )) for msg in a_to_b
        ]

        history_b_to_a = [
            MessageEntity(MessageSchema(
                sender_id=msg.sender_id,
                receiver_id=msg.receiver_id,
                content=msg.content,
                sent_at=msg.sent_at,
                delivered_at=msg.delivered_at,
                status=msg.status
            )) for msg in b_to_a
        ]

        return {"history": history_a_to_b + history_b_to_a}