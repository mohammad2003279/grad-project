from users.entities.user_entites import UserEntity
from users.repositories.change_basic_information_repo import ChangeInfoRepository, ChangePasswordRepository, ChangeForgetPasswordRepository
from core.exceptions.exceptions import EntityNotFound
from sqlalchemy.orm import Session
from utils.models import User, Validated_email
import redis
import json

class ChangeInfoRepositorySQL(ChangeInfoRepository):
    def __init__(self, session: Session):
        self.session = session

    def update(self, update_info_entity: UserEntity):
        db_model = self.session.query(User).filter_by(user_id=update_info_entity.user_id).first()
        db_model.f_name = update_info_entity.f_name # type: ignore
        db_model.l_name = update_info_entity.l_name # type: ignore
        self.session.commit()
        self.session.refresh(db_model)


class ChangePasswordSQL(ChangePasswordRepository):
    def __init__(self, session: Session):
        self.session = session

    
    def get_by_email(self, user_id: int):
        db_model = self.session.query(User).filter_by(user_id=user_id).first()
        return UserEntity(
            user_id= db_model.user_id, # type: ignore
            f_name = db_model.f_name, # type: ignore
            l_name = db_model.l_name, # type: ignore
            hashed_password = db_model.hashed_password # type: ignore
        )


    def update(self, udpate_password_entity: UserEntity):
        db_model = self.session.query(User).filter_by(user_id=udpate_password_entity.user_id).first()
        db_model.hashed_password = udpate_password_entity.hashed_password # type: ignore
        self.session.commit()
        self.session.refresh(db_model)


class ChangeForgetPasswordRepositorySQL(ChangeForgetPasswordRepository):
    def __init__(self, session : Session):
        self.redis_server = redis.Redis(host="localhost", port=6379, db=0)
        self.session = session
    def get_by_email(self, email: str):
        cache_response = self.redis_server.get(f"UserEmail:{email}")
        if cache_response is None:
            raise EntityNotFound()
        data =  dict(json.loads(cache_response)) # type: ignore
        db_model = self.session.query(User).filter_by(email=email).first()
        data["hashed_password"] = db_model.hashed_password # type: ignore
        return data
    
    def delete(self, email: str):
        self.redis_server.delete(f"UserEmail:{email}")

    def update(self, udpate_password_entity: UserEntity):
        db_model = self.session.query(User).filter_by(email=udpate_password_entity.email).first() # type: ignore
        db_model.hashed_password = udpate_password_entity.hashed_password # type: ignore
        self.session.commit()
        self.session.refresh(db_model)