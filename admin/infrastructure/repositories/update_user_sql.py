from admin.repositories.update_user import SuspensionUserRepositories,AcceptionDoctorRepositories
from sqlalchemy.orm import Session
from utils.models import User,Role_doctor,RefreshTokenModel
from core.exceptions.exceptions import EntityNotFound

class SuspensionUserRepositoriesSql(SuspensionUserRepositories):
    def __init__(self, session: Session):
        self.session = session

    def suspensionUser(self, user_id: int):
        db_model = self.session.query(User).filter_by(user_id=user_id).first()
        db_refresh=self.session.query(RefreshTokenModel).filter_by(user_id=user_id).first()
        if db_model:
            db_model.suspension = not db_model.suspension
            db_refresh.revoked = not db_refresh.revoked
            self.session.commit()
            return {
                "message": "User has been suspended."
                if db_model.suspension else "User has been unsuspended."
            }
        else:
            raise EntityNotFound


class AcceptionDoctorRepositoriesSql(AcceptionDoctorRepositories):
    def __init__(self, session: Session):
        self.session = session

    def acceptionDoctor(self, doctor_id: int):
        db_model = self.session.query(Role_doctor).filter_by(doctor_id=doctor_id).first()
        if db_model:
            db_model.accepted = not db_model.accepted
            self.session.commit()
            return {
                "message": "Doctor has been accepted."
                if db_model.accepted else "Doctor has been unaccepted."
            }
        else:
            raise EntityNotFound
