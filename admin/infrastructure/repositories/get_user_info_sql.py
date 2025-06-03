from sqlalchemy.orm import Session
from utils.models import User,Role_doctor
from admin.repositories.get_user_info import ReadUsersInfoRepositories
from admin.entities.admin_entities import AdminUserEntities,AdminDoctorEntities
from core.exceptions.exceptions import EntityNotFound,WrongRole
import redis
import json

class ReadUsersInfoRepositoriesSql(ReadUsersInfoRepositories):
    def __init__(self, session: Session):
        self.session = session
        self.redis_server = redis.Redis(host="localhost", port=6379, db=0)

    def get_by_id(self, user_id: int):
        cache_key = f"UserID:{user_id}"
        cached_data = self.redis_server.get(cache_key)
        if cache_key:
            data_body = dict(json.loads(cached_data)) # type: ignore
            return AdminUserEntities(
                    user_id=data_body["user_id"], # type: ignore
                    email=data_body["email"], # type: ignore
                    name=data_body["f_name"]+' '+data_body["l_name"], # type: ignore
                    role=data_body["role"], # type: ignore
                    signup_date=data_body["signup_date"], # type: ignore
                    suspension=data_body["suspension"] # type: ignore
                )
        db_models = self.session.query(User).filter_by(user_id=user_id).first()
        if db_models:
            data_body = {"user_id": db_model.user_id, "f_name": db_model.f_name, "l_name": db_model.l_name, # type: ignore
                      "role": db_model.role, "age": db_model.age, "profile_picture": db_model.profile_picture, "email": db_model.email, # type: ignore
                      "signup_date": str(db_model.signup_date), "suspension": db_model.suspension} # type: ignore
            self.redis_server.set(cache_key, json.dumps(data_body), ex=300)
            return AdminUserEntities(
                    user_id=db_models.user_id, # type: ignore
                    email=db_models.email, # type: ignore
                    name=db_models.f_name+' '+db_models.l_name, # type: ignore
                    role=db_models.role, # type: ignore
                    signup_date=db_models.signup_date, # type: ignore
                    suspension=db_models.suspension # type: ignore
                )
        else:
            raise EntityNotFound

    def get_by_role(self, role: str):
        role = role.casefold()
        if role not in ('doctor', 'patient'):
            raise WrongRole
        return self.session.query(User).filter(User.role==role).all()


    def get_all_users_info(self):
        db_models = self.session.query(User).all()
        if not db_models:
            raise EntityNotFound
        return [
            AdminUserEntities(
                user_id=user.user_id,
                email=user.email,
                name=user.f_name + ' ' + user.l_name,
                role=user.role,
                signup_date=user.signup_date,
                suspension=user.suspension,
            )
            for user in db_models
        ]
