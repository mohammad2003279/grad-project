from auth.entities.user_entities import CheckUserRequest, CheckUserExistRequest
from auth.repositories.check_user_request_repository import CheckUserRequestRepository, CheckUserExistRepository
from sqlalchemy.orm import Session
from utils.models import User
from core.exceptions.exceptions import UnAuthorizedAccess


class CheckUserRequestRepositorySQL(CheckUserRequestRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> bool:
        db_model = self.session.query(User).filter_by(email = email).first()
        if db_model is not None:
            return True
        return False


class CheckUserExistRepositorySQL(CheckUserExistRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> CheckUserExistRequest:
        db_model = self.session.query(User).filter_by(email = email).first()
        if db_model is None:
            raise UnAuthorizedAccess() #User not found
        return CheckUserExistRequest(
            user_id = db_model.user_id,
            hashed_password = db_model.hashed_password,
            f_name = db_model.f_name,
            l_name = db_model.l_name,
            role = db_model.role,
            suspended = db_model.suspension
        )
