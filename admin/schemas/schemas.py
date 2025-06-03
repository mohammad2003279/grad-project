from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UsersInfo(BaseModel):
    email: Optional[str] = None
    f_name: Optional[str] = None
    l_name: Optional[str] = None
    role: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    signup_date: Optional[datetime] = None
    user_id: int
    suspension: Optional[bool] = None


class DoctorInfo(BaseModel):
    numbers_of_records: Optional[int] = None
    doctor_id: int
    rating_avg: Optional[float] = None
    accepted: Optional[bool] = None

class RecordsInfo(BaseModel):
    img_id:int
    user_id: Optional[int]=None
    test_result:Optional[str]=None
    test_date:Optional[datetime]=None
    