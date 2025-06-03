from users.repositories.check_user_validated_code import CheckUserValidatedCode
from core.exceptions.exceptions import RequestNotFound
from utils.models import Validated_email
import redis
import json


class CheckUserValidatedCodeSQL(CheckUserValidatedCode):
    def __init__(self):
        self.redis_server = redis.Redis(host="localhost", port=6379, db=0)

    def get_by_email(self, email):
        cached_data = self.redis_server.get(f"UserEmail:{email}")
        if cached_data is None:
            raise RequestNotFound
        return dict(json.loads(cached_data)) # type: ignore
    
    def delete(self, email: str) -> None:
        self.redis_server.delete(f"UserEmail:{email}")