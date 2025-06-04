from users.repositories.user_information_repository import UserInformationRepository
from sqlalchemy.orm import Session
from utils.models import User
from users.entities.user_entites import UserEntity
import redis
import json
from core.exceptions.exceptions import EntityNotFound
class UserInformationRepositorySQL(UserInformationRepository):
    def __init__(self, session: Session):
        self.session = session
        self.redis_server = redis.Redis(host="localhost", port=6379, db=0)

    def add(self, user_id: int, path: str):
        db_model = self.session.query(User).filter_by(user_id=user_id).first()
        if not db_model:
            raise ValueError(f"User with id {user_id} not found.")
        db_model.profile_picture = path # type:ignore
        self.session.commit()
        self.session.refresh(db_model)

    def get_profile_pic(self, user_id: int) -> str:
        cache_key = f"UserID:{user_id}"
        cached_data = self.redis_server.get(cache_key)
        if cached_data:
            data_body = json.loads(cached_data) # type: ignore
            return data_body["profile_picture"]
        db_model = self.session.query(User).filter_by(user_id=user_id).first()
        if not db_model:
            raise EntityNotFound
        data_body = {"user_id": db_model.user_id, "f_name": db_model.f_name, "l_name": db_model.l_name, # type: ignore
                      "role": db_model.role, "age": db_model.age, "profile_picture": db_model.profile_picture, "email": db_model.email,
                      "signup_date": str(db_model.signup_date), "suspension": db_model.suspension} # type: ignore
        self.redis_server.set(cache_key, json.dumps(data_body), ex=300)
        return db_model.profile_picture # type:ignore

    def get_basic_info(self, user_id: int) -> UserEntity:
        cache_key = f"UserID:{user_id}"
        cached_data = self.redis_server.get(cache_key)
        if cached_data:
            data_body = dict(json.loads(cached_data)) # type: ignore
            return UserEntity(
            user_id=data_body["user_id"],
            f_name=data_body["f_name"],
            l_name=data_body["l_name"],
            role=data_body["role"],
            age=data_body["age"]
        )
        db_model = self.session.query(User).filter_by(user_id=user_id).first()
        data_body = {"user_id": db_model.user_id, "f_name": db_model.f_name, "l_name": db_model.l_name, # type: ignore
                      "role": db_model.role, "age": db_model.age, "profile_picture": db_model.profile_picture, "email": db_model.email, # type: ignore
                      "signup_date": str(db_model.signup_date), "suspension": db_model.suspension} # type: ignore
        self.redis_server.set(cache_key, json.dumps(data_body), ex=300)
        return UserEntity(
            user_id=db_model.user_id, # type: ignore
            f_name=db_model.f_name, # type: ignore
            l_name=db_model.l_name, # type: ignore
            role=db_model.role, # type: ignore
            age=db_model.age # type: ignore
        )
