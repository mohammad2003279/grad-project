from sqlalchemy.orm import Session
from users.repositories.cv_doctor import DoctorRepository
from utils.models import Role_doctor
class DoctorRepositoryImpl(DoctorRepository):
    def __init__(self, session: Session):
        self.session = session

    def upload_cv(self, doctor_id: int, cv_path: str) -> None:
        doctor = self.session.query(Role_doctor).filter_by(doctor_id=doctor_id).first()
        doctor.cv_path = cv_path
        self.session.commit()