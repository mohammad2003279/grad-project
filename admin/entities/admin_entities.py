from admin.schemas.schemas import RecordsInfo
from datetime import datetime

class AdminUserEntities:
    def __init__(self,user_id: int,email: str,name: str,role: str,signup_date:datetime,suspension: bool,acception: bool = None  ):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.role = role
        self.signup_date = signup_date
        self.suspension = suspension

    def is_suspended(self):
        return self.suspension


class AdminDoctorEntities:
    def __init__(
        self,
        name:str,
        doctor_id: int,
        rating_avg: float,
        acception: bool,

    ):
        self.name=name
        self.doctor_id = doctor_id
        self.rating_avg = rating_avg
        self.acception = acception


    def is_accepted(self):
        return self.acception
#R stands for records
class AdminRecordsEntities:
    def __init__(self,records_info:RecordsInfo):
        self.records_info=records_info

