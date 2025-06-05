from sqlalchemy.orm import Session
from users.entities.user_entites import AppointmentEntity
from users.repositories.get_user_appointments import AppointmentPatientRepo
from utils.models import AppointmentModel,User
from core.exceptions.exceptions import EntityNotFound

class AppointmentPatientRepoSql(AppointmentPatientRepo):
    def __init__(self, session: Session):
        self.session = session
        
    def get_all_appointments(self, user_id: int):
        appointments = self.session.query(AppointmentModel).filter_by(user_id=user_id).all()
        if appointments ==[]:
            raise EntityNotFound
        result = []
        for a in appointments:
            # Fetch doctor and patient names
            doctor = self.session.query(User).filter_by(user_id=a.doctor_id).first()
            patient = self.session.query(User).filter_by(user_id=a.user_id).first()

            # Optional: handle if user not found
            if not doctor or not patient:
                continue

            result.append(
                AppointmentEntity(
                    appointment_id=a.id,
                    user_id=a.user_id,
                    doctor_id=a.doctor_id,
                    appointment_date=a.appointment_date,
                    status=a.status,
                    doctorname=doctor.f_name + ' ' + doctor.l_name,
                    patientname=patient.f_name + ' ' + patient.l_name
                )
            )
        
        return result
    def cancel_appointments(self, appointment_id: int,user_id:int):
        appointment = self.session.query(AppointmentModel).filter_by(id=appointment_id).first()
        if appointment is None:
            raise EntityNotFound
        if user_id == appointment.user_id or user_id==appointment.doctor_id:
            self.session.delete(appointment)
            self.session.commit()
            return "appointments has canceled successfully"
        else:
            raise EntityNotFound