from users.repositories.appointment_repository import IAppointmentRepository
from users.entities.user_entites import AppointmentEntity
from typing import List

class AppointmentUseCase:
    def __init__(self, repo: IAppointmentRepository):
        self.repo = repo

    def create_appointment(self, appointment: AppointmentEntity,user_id:int) -> AppointmentEntity:
        return self.repo.create_appointment(appointment,user_id)

    def list_appointments_for_doctor(self, doctor_id: int) -> List[AppointmentEntity]:
        return self.repo.get_all_appointments(doctor_id)

    def accept_appointment(self, appointment_id: int) -> AppointmentEntity:
        return self.repo.accept_appointment(appointment_id)
