from users.repositories.user_information_repository import UserInformationRepository
from sqlalchemy.orm import Session
from utils.models import User
from users.entities.user_entites import UserEntity
from core.exceptions.exceptions import EntityNotFound

class UserInformationRepositorySQL(UserInformationRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, user_id: int, path: str):
        db_model = self.session.query(User).filter_by(user_id=user_id).first()
        if not db_model:
            raise ValueError(f"User with id {user_id} not found.")
        db_model.profile_picture = path  # type:ignore
        self.session.commit()
        self.session.refresh(db_model)

    def get_profile_pic(self, user_id: int) -> str:
        db_model = self.session.query(User).filter_by(user_id=user_id).first()
        if not db_model:
            raise EntityNotFound
        return db_model.profile_picture  # type:ignore

    def get_basic_info(self, user_id: int) -> UserEntity:
        db_model = self.session.query(User).filter_by(user_id=user_id).first()
        if not db_model:
            raise EntityNotFound
        return UserEntity(
            user_id=db_model.user_id,  # type:ignore
            f_name=db_model.f_name,    # type:ignore
            l_name=db_model.l_name,    # type:ignore
            role=db_model.role,        # type:ignore
            age=db_model.age           # type:ignore
        )
