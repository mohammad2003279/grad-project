from users.repositories.get_most_avg_rate import DoctorRepository

class DoctorUseCase:
    def __init__(self, doctor_repo:DoctorRepository):
        self.doctor_repo = doctor_repo

    def get_top_five_doctors(self):
        return self.doctor_repo.get_top_rated_doctors()
