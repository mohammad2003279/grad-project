from datetime import datetime

class VerificationRequest:
    def __init__(self, email: str, verification_code: str, expires_at: datetime):
        self.email = email
        self.verification_code = verification_code
        self.expires_at = expires_at

    def verification_code_is_valid(self, verification_code: str):
        if not verification_code == self.verification_code :
            return 1
        elif not datetime.utcnow() < self.expires_at:
            return 2

