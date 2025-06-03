from auth.repositories.verification_request_accepted import VerificationRequestAccepted
from sqlalchemy.orm import Session
from utils.models import Validated_email

class VerificationRequestAcceptedSQL(VerificationRequestAccepted):
    def __init__(self, session: Session):
        self.session = session

    def add(self, email: str):
        db_model = Validated_email(
            email = email
        )
        self.session.add(db_model)
        self.session.commit()