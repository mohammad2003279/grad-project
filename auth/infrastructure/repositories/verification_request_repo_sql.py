from auth.entities.verification_request import VerificationRequest
from auth.repositories.verification_request_repository import VerificationRequestRepository 
from sqlalchemy.orm import Session
from utils.models import Check_request
from core.exceptions.exceptions import RequestNotFound
from utils.models import User
from datetime import datetime, timedelta
import redis
import json


class VerificationRequestRepositorySQL(VerificationRequestRepository):
    def __init__(self, session: Session):# session: Session):
        self.session = session
        self.redis_server = redis.Redis(host="localhost", port=6379, db=0)
    
    def add(self, request: VerificationRequest) -> None:
        cache_key = f"UserEmail:{request.email}"
        data_body = {"v_code": request.verification_code, "exp": str(request.expires_at), "validated": "false"}
        self.redis_server.set(cache_key, json.dumps(data_body), ex=900)

    def get_by_email(self, email: str) -> dict:
        cached_data = self.redis_server.get(f"UserEmail:{email}")
        if cached_data is None:
            raise RequestNotFound
        data_body = dict(json.loads(cached_data)) # type: ignore
        return data_body

    def delete(self, email: str) -> None:
        self.redis_server.delete(f"UserEmail:{email}")

    def update(self, email: str) -> None:
        cache_key = f"UserEmail:{email}"
        cached_data = self.redis_server.get(f"UserEmail:{email}")
        data_body = dict(json.loads(cached_data)) # type: ignore
        data_body["validated"] = "true"
        self.redis_server.set(cache_key, json.dumps(data_body), ex=1800)
    def check_exist(self, email):
        db_model = self.session.query(User).filter(User.email == email).first()
        if db_model is None:
            return False
        return True

class ForgetPasswordVCodeRepositorySQL(VerificationRequestRepositorySQL):
    def __init__(self, session: Session):
        self.session = session
        
    def add(self, request: VerificationRequest):
        db_model = Check_request(
            email = request.email,
            v_code = request.verification_code,
            expiration = request.expires_at
        )
        self.session.add(db_model)
        self.session.commit()