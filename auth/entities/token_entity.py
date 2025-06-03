from datetime import datetime

class RefreshTokenEntity:
    def __init__(self, token: str, user_id: int, expires_at: datetime, revoked: bool):
        self.token = token
        self.user_id = user_id
        self.expires_at = expires_at
        self.revoked = revoked

    def is_expired(self):
        return datetime.utcnow() > self.expires_at
    
    def is_revoked(self):
        return self.revoked