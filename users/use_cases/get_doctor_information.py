from users.repositories.doctor_information_repository import DoctorInformationRepository, DoctorsRepository
from core.exceptions.exceptions import UnAuthorizedAccess, UnSupportedFormat, UserNotFound

class GetDoctorInformation:
    def __init__(self, repo: DoctorInformationRepository):
        self.repo = repo
        
    def execute(self, doctor_id: int):
        user_flag = self.repo.get_by_email(doctor_id=doctor_id)
        if not user_flag.role.casefold() == 'doctor':
            raise UnAuthorizedAccess()
        return self.repo.get_acceptation_result(doctor_id=doctor_id)
    


class GetDoctorBio:
    def __init__(self, repo: DoctorInformationRepository):
        self.repo = repo

    def execute(self, doctor_id:int):
        return self.repo.get_doctor_bio(doctor_id=doctor_id)
    

class GetTopRatedDoctors:
    def __init__(self, repo: DoctorsRepository):
        self.repo = repo

    def execute(self, limit:int = 5):
        return self.repo.get_top_rated_doctors(limit)
    
class RateDoctor:
    def __init__(self, repo: DoctorInformationRepository):
        self.repo = repo
    def execute(self,doctor_id: int, rate: int):
        try:
            if rate <= 0 or rate > 5:
                raise UnSupportedFormat()
            self.repo.rate_doctor(doctor_id, rate)
        except UserNotFound:
            raise UserNotFound()