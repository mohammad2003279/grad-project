from sqlalchemy.orm import Session
from users.entities.user_entites import AppointmentEntity
from users.repositories.appointment_repository import IAppointmentRepository
from utils.models import AppointmentModel,User,Role_doctor
from core.exceptions.exceptions import EntityNotFound,DoctorNotAccepted

class AppointmentRepositoryImpl(IAppointmentRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_appointment(self, appointment: AppointmentEntity, user_id: int) -> AppointmentEntity:
        db_appointment = AppointmentModel(
            user_id=user_id,
            doctor_id=appointment.doctor_id,
            appointment_date=appointment.appointment_date,
            status=appointment.status,
        )

        doctor = self.session.query(Role_doctor).filter_by(doctor_id=appointment.doctor_id).first()
        if doctor is None:
            raise EntityNotFound
        elif doctor.accepted is False:
            raise DoctorNotAccepted

        self.session.add(db_appointment)
        self.session.commit()
        self.session.refresh(db_appointment)

        # Get patient info
        patient = self.session.query(User).filter_by(user_id=user_id).first()

        # Get doctor info using the user_id from Role_doctor
        doctor_user = self.session.query(User).filter_by(user_id=doctor.doctor_id).first()

        return AppointmentEntity(
            appointment_id=db_appointment.id,
            user_id=user_id,
            doctor_id=db_appointment.doctor_id,
            appointment_date=db_appointment.appointment_date,
            status=db_appointment.status,
            patientname=f"{patient.f_name} {patient.l_name}",
            doctorname=f"{doctor_user.f_name} {doctor_user.l_name}"
        )

    def get_all_appointments(self, doctor_id: int):
        appointments = self.session.query(AppointmentModel).filter_by(doctor_id=doctor_id).all()
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
    def accept_appointment(self, appointment_id: int) -> AppointmentEntity:
        appointment = self.session.query(AppointmentModel).filter_by(id=appointment_id).first()
        if appointment is None:
            raise EntityNotFound
        appointment.status = "accepted"
        self.session.commit()
        self.session.refresh(appointment)
        doctorname = self.session.query(User).filter_by(user_id=appointment.doctor_id).first()
        patientname=self.session.query(User).filter_by(user_id=appointment.user_id).first()
        return AppointmentEntity(
            patientname=patientname.f_name+' '+patientname.l_name,
            appointment_id=appointment.id,
            user_id=appointment.user_id,
            doctor_id=appointment.doctor_id,
            appointment_date=appointment.appointment_date,
            status=appointment.status,
            doctorname=doctorname.f_name+' '+doctorname. l_name
        )