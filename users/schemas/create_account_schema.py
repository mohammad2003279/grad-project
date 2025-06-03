from pydantic import BaseModel
from datetime import datetime

class CreateAccountSchema(BaseModel):
    email: str
    f_name: str
    l_name: str
    hashed_password: str
    role: str
    age: int
    sex: str
    
class AppointmentCreateRequest(BaseModel):
    doctor_id: int
    
class AppointmentResponse(BaseModel):
    appointment_id: int
    user_id: int
    doctor_id: int
    appointment_date: datetime
    status: str
    doctorname:str
    patientname:str