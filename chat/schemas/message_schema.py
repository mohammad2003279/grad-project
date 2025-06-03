from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageSchema(BaseModel):
    sender_id : int
    receiver_id: int
    content: str
    sent_at: datetime
    delivered_at: Optional[datetime] = None
    status: str = 'pending'