from users.repositories.get_user_appointments import AppointmentPatientRepo
from users.entities.user_entites import AppointmentEntity
from typing import List

class AppointmentsUseCase:
    def __init__(self, repo: AppointmentPatientRepo):
        self.repo = repo

    def list_appointments_for_patient(self, user_id: int) -> List[AppointmentEntity]:
        return self.repo.get_all_appointments(user_id)

    def cancel_appointments(self, appointment_id: int,user_id:int) -> None:
        return self.repo.cancel_appointments(appointment_id,user_id)
