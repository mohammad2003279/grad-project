from datetime import datetime
from users.schemas.schema import RecordsInfo
class UserEntity:
    def __init__(self, user_id: int = None, f_name: str = None, l_name: str = None, hashed_password: str = None, status: bool = None, #type: ignore
                  role: str = None, age: int = None, email: str = None, profile_picture: str = None): #type: ignore
        self.user_id = user_id
        self.f_name = f_name
        self.l_name = l_name
        self.hashed_password = hashed_password
        self.status = status
        self.role = role
        self.age = age
        self.email = email
        self.profile_picture = profile_picture

    def is_active(self):
        return self.status
    
    
    
class DoctorEntity:
    def __init__(self, doctor_id: int = None, accepted: bool = None, bio: str = None, rating_avg: float = None): #type: ignore
        self.doctor_id = doctor_id
        self.accepted = accepted
        self.bio = bio #type: ignore
        self.rating_avg = rating_avg #type: ignore
    def is_accepted(self):
        return self.accepted
    def bio(self):
        return self.bio
    def rating_avg(self):
        return self.rating_avg


class AppointmentEntity:
    def __init__(self,patientname:str,doctorname:str, appointment_id: int = None, user_id: int = None, doctor_id: int = None, appointment_date: datetime = None, status: str = 'pending'): #type: ignore
        self.appointment_id = appointment_id
        self.user_id = user_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.status = status
        self.patientname=patientname
        self.doctorname=doctorname


class ReportEntity:
    def __init__(self,user_id:int,user_reported:int,description:str,report_type:str):
        self.user_id = user_id
        self.user_reported = user_reported
        self.discreption = discreption
        self.report_type = report_type


class UserRecordsEntities:
    def __init__(self,records_info:RecordsInfo):
        self.records_info=records_info
