from sqlalchemy.orm import Session
from utils.models import User, Role_doctor
from admin.repositories.get_doctors_by_acception import GetDoctorsByAcception
from admin.entities.admin_entities import AdminDoctorEntities
from core.exceptions.exceptions import EntityNotFound

class GetDoctorsByAcceptionRepo(GetDoctorsByAcception):
    def __init__(self, session: Session):
        self.session = session

    def get_doctors_by_acception(self, acception: bool):
        doctors = self.session.query(Role_doctor).filter_by(accepted=acception).all()
        if not doctors:
            return None

        result = []
        for doctor_role in doctors:
            doctor = self.session.query(User).filter_by(user_id=doctor_role.doctor_id).first()
            if not doctor:
                continue  

            result.append(
                AdminDoctorEntities(
                    name=f"{doctor.f_name} {doctor.l_name}",
                    doctor_id=doctor_role.doctor_id,
                    rating_avg=doctor_role.rating_avg,
                    acception=doctor_role.accepted
                )
            )

        return result
