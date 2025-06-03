from infrastructure.db.database import Base
from sqlalchemy import LargeBinary, TEXT, VARCHAR, Column, Integer, String, Boolean, ForeignKey, DateTime,Float, Enum as PgEnum
from datetime import datetime
from zoneinfo import ZoneInfo
from utils.report_type import ReportType,StatusType
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer,index=True, autoincrement=True,primary_key=True)
    f_name = Column(VARCHAR(25), nullable=False)
    l_name = Column(VARCHAR(25), nullable=False)
    email = Column(VARCHAR(100), unique=True, nullable=False)
    hashed_password = Column(TEXT, nullable=False)
    age=Column(Integer,nullable=False)
    sex = Column(VARCHAR(10), nullable=False)
    role = Column(VARCHAR(10), nullable=False,default='patient')
    profile_picture = Column(VARCHAR(250))
    signup_date = Column(DateTime)
    suspension = Column(Boolean)


class Test_records(Base):
    __tablename__ = 'test_records'

    img_id = Column(Integer, index=True,autoincrement=True, primary_key=True)
    img_path = Column(TEXT, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    test_result = Column(VARCHAR(5), nullable=False)
    test_date = Column(DateTime)
    test_ratio = Column(Float, nullable=False)

class Role_doctor(Base):
    __tablename__ = "role_doctor"

    number_of_records = Column(Integer, index=True, autoincrement=True, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    bio = Column(VARCHAR(300), nullable = True)
    rating_avg = Column(Float)
    accepted = Column(Boolean)
    cv_path = Column(TEXT, nullable=True)  
    number_of_review = Column(Integer, nullable=False)
    rating_sum = Column(Integer, nullable=False)
    
class Check_request(Base):
    __tablename__ = "check_request"
    email = Column(TEXT, primary_key=True)
    v_code = Column(VARCHAR(6))
    expiration = Column(DateTime)

class Validated_email(Base):
    __tablename__ = 'validated_email'
    email = Column(TEXT, primary_key=True)


class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True,index=True)
    jwt_token = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    expires_at = Column(DateTime)
    revoked = Column(Boolean, default = False)


class AppointmentModel(Base):
    __tablename__ = 'appointments'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)  # referencing users, not a doctors table
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String, default='pending')


class Messages(Base):
    __tablename__ = "messages"
    message_id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)
    content = Column(TEXT, nullable=False)
    sent_at = Column(DateTime, nullable=False)
    delivered_at = Column(DateTime, nullable=False)
    status = Column(VARCHAR(25), nullable=False)

class ReportHistory(Base):
    __tablename__ = "report_logs"

    id = Column(Integer, primary_key=True, index=True)
    reporter_id = Column(Integer, nullable=False)
    reported_user_id = Column(Integer, nullable=True)
    report_type = Column(PgEnum(ReportType, name="report_type_enum"), nullable=False)
    description = Column(TEXT, nullable=False)
    status = Column(PgEnum(StatusType, name="status_enum"), nullable=False, default=StatusType.pending)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(ZoneInfo("Asia/Amman")))
    updated_at = Column(DateTime, nullable=True, default=lambda: datetime.now(ZoneInfo("Asia/Amman")))
    