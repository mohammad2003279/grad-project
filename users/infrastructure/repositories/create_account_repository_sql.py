from users.repositories.create_account_request_repository import CreateAccountRequestRepository, CreateDoctorAccountRepository
from sqlalchemy.orm import Session
from users.schemas.create_account_schema import CreateAccountSchema
from utils.models import User, Role_doctor
from datetime import datetime


class CreateAccountRequestRepositorySQL(CreateAccountRequestRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, cam: CreateAccountSchema):
        db_model = User(
            email = cam.email,
            f_name = cam.f_name,
            l_name = cam.l_name,
            hashed_password = cam.hashed_password,
            age = cam.age,
            sex = cam.sex,
            role = cam.role,
            signup_date = datetime.now(),
            suspension = False
        )
        self.session.add(db_model)
        self.session.commit()
        
class CreateAccountDoctorSQL(CreateDoctorAccountRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, email: str):
        user_db = self.session.query(User).filter_by(email=email).first()
        db_model = Role_doctor(
            doctor_id = user_db.user_id,
            rating_avg = 0.0,
            accepted = False
        )
        self.session.add(db_model)
        self.session.commit()