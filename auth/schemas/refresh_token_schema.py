from pydantic import BaseModel
from datetime import datetime


class RefreshTokenSchema(BaseModel):
    token: str
    user_id: int
    expires_at: datetime
    revoked: bool