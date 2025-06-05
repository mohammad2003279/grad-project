#############################################################################################################################
###### FastAPI packages #####################################################################################################
from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import FileResponse
#############################################################################################################################
######### infrastructure ####################################################################################################
from infrastructure.db.dependencies import db_dependency
#############################################################################################################################
########## Entities #########################################################################################################
from users.entities.user_entites import AppointmentEntity
#############################################################################################################################
####### Repository implementation ###########################################################################################
from users.infrastructure.repositories.create_account_repository_sql import CreateAccountRequestRepositorySQL, CreateAccountDoctorSQL
from users.infrastructure.repositories.check_user_validated_code_sql import CheckUserValidatedCodeSQL
from users.infrastructure.repositories.change_basic_information_repo import ChangeInfoRepositorySQL, ChangePasswordSQL, ChangeForgetPasswordRepositorySQL
from users.infrastructure.repositories.change_bio_repository_sql import ChangeBioRepositorySQL
from users.infrastructure.repositories.doctor_information_repository_sql import DoctorInformationRepositorySQL, DoctorsRepositorySQL
from users.infrastructure.repositories.user_information_repository_sql import UserInformationRepositorySQL
from users.infrastructure.repositories.appointment_repository_Sql import AppointmentRepositoryImpl
from users.infrastructure.repositories.cv_doctor_sql import DoctorRepositoryImpl
from users.infrastructure.repositories.reports_sql import UserReportRepositorySql
from users.infrastructure.repositories.get_top_doctor_rating import DoctorRepositoryImpls
from users.infrastructure.repositories.get_user_appointments_sql import AppointmentPatientRepoSql
#############################################################################################################################
######## Use cases###########################################################################################################
from users.use_cases.check_account_validated import CheckAccountValidation
from users.use_cases.create_account import CreateAccountRequest
from users.use_cases.change_basic_information import ChangeBasicInformation, ChangePassword, ForgetPassword
from users.use_cases.change_bio import ChangeBio
from users.use_cases.get_doctor_information import GetDoctorInformation, GetDoctorBio, GetTopRatedDoctors, RateDoctor
from users.use_cases.user_information_operations import PostUserPicture, GetUserPicture, GetBasicInformation
from users.use_cases.appointmentation import AppointmentUseCase
from users.use_cases.validate_user import validate_doctor_role
from users.use_cases.upload_cv import UploadCVUseCase
from users.use_cases.report_a_user import ReportUsers
from users.use_cases.reports_type import ReportType
from users.use_cases.get_top_rating import DoctorUseCase
from users.use_cases.user_appointments import AppointmentsUseCase
#############################################################################################################################
######## Schemas ############################################################################################################
from users.schemas.create_account_schema import CreateAccountSchema, AppointmentCreateRequest, AppointmentResponse
#############################################################################################################################
######### Exceptions ########################################################################################################
from core.exceptions.http_exceptions import HTTPUnAuthorizedCreateAccount, HTTPPasswordNewNotValid, HTTPPassswordNotMatch, HTTPUnAuthorizedUser, HTTPUnsupportedFileFormat, HTTPFailedToUploadPicture, HTTPFailedToFetchImage, HTTPInvalidVerificationCode, HTTPUserNotFound, HTTPDoctorNotAccepted, HTTPDoctorNotFound, HTTPNoAppointmentsFound, HTTPNoAppointmentsNotFound, HTTPFailedToUploadCV
from core.exceptions.exceptions import UnAuthorizedCreateAccount, PasswordNewNotValid, PasswordNotMatch, UnAuthorizedAccess, AppException, UnSupportedFormat, EntityNotFound, UserNotFound, FailedToSaveFile, DoctorNotAccepted
#############################################################################################################################
########## Dependencies #####################################################################################################
from users.api.dependencies import user_dependency
#############################################################################################################################
########### General Packages ################################################################################################
from fastapi import Depends
from auth.api.dependency import get_current_user
from typing import List
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import shutil
from core.src.rate_limitting import limiter
#############################################################################################################################
#############################################################################################################################

router = APIRouter(
    prefix='/users',
    tags=['Users domain']
)

@router.post("/create-account/", status_code=201)
@limiter.limit("5/minute")
async def create_account(request: Request, create_account_request: CreateAccountSchema, db: db_dependency):
    try:
        repo_check = CheckUserValidatedCodeSQL()
        use_case_check = CheckAccountValidation(repo_check)
        use_case_check.execute(create_account_request.email.casefold())
    except UnAuthorizedCreateAccount:
        raise HTTPUnAuthorizedCreateAccount()

    repo_create_account = CreateAccountRequestRepositorySQL(db)
    repo_create_doctor = CreateAccountDoctorSQL(db)
    use_case_create_account = CreateAccountRequest(repo_create_account, repo_create_doctor)
    use_case_create_account.execute(create_account_request)
    return {"message": "user created successfully"}

@router.post("/upload-profile-picture/", status_code=201)
@limiter.limit("10/minute")
async def upload_profile_picture(request: Request, user: user_dependency, db: db_dependency, file: UploadFile = File(...)):
    try:
        repo = UserInformationRepositorySQL(db)
        use_case = PostUserPicture(repo)
        await use_case.execute(user["id"], file)
        return {"message":"pictuire uploaded successfully"}
    except UnSupportedFormat:
        raise HTTPUnsupportedFileFormat()
    except AppException:
        raise HTTPFailedToUploadPicture()

@router.put("/update-basic-information/{f_name}/{l_name}", status_code=201)
@limiter.limit("10/minute")
async def update_basic_information(request: Request, f_name: str, l_name: str, db: db_dependency, user: dict = Depends(get_current_user)):
    repo = ChangeInfoRepositorySQL(db)
    use_case = ChangeBasicInformation(repo)
    use_case.execute(f_name, l_name, user["id"])
    return {"Message": "User credentials updated successfully."}

@router.put("/update/password/{old_password}/{new_password}", status_code=201)
@limiter.limit("5/minute")
async def update_user_password(request: Request, old_password: str, new_password: str, db: db_dependency, user: dict = Depends(get_current_user)):
    try:
        repo = ChangePasswordSQL(db)
        use_case = ChangePassword(repo)
        use_case.execute(user["id"], old_password, new_password)
        return {"Message": "Password has been changed successfully."}
    except PasswordNotMatch:
        raise HTTPPassswordNotMatch()
    except PasswordNewNotValid:
        raise HTTPPasswordNewNotValid()

@router.put("/info/update-forget-password", status_code=201)
@limiter.limit("3/minute")
async def update_password(request: Request, new_password: str, email: str, db: db_dependency):
    try:
        repo = ChangeForgetPasswordRepositorySQL(db)
        use_case = ForgetPassword(repo)
        use_case.execute(email, new_password)
        return {"Message": "Password has been changed successfully."}
    except PasswordNewNotValid:
        raise HTTPPasswordNewNotValid()
    except EntityNotFound:
        raise HTTPInvalidVerificationCode()

@router.put("/update-bio/{bio}", status_code=201)
@limiter.limit("10/minute")
async def update_bio(request: Request, bio: str, db: db_dependency, user: dict = Depends(get_current_user)):
    try:
        repo = ChangeBioRepositorySQL(db)
        use_case = ChangeBio(repo)
        use_case.execute(bio, user["id"])
        return {"Message": {"Bio updated successfully"}}
    except UnAuthorizedAccess:
        raise HTTPUnAuthorizedUser()

@router.get("/doctor-acceptation-result", status_code=200)
async def get_doctor_result(db: db_dependency, user: dict = Depends(get_current_user)):
    try:
        repo = DoctorInformationRepositorySQL(db)
        use_case = GetDoctorInformation(repo)
        return {"Result": use_case.execute(user["id"])}
    except UnAuthorizedAccess:
        raise HTTPUnAuthorizedUser()

@router.get("/info/doctor-bio", status_code=200)
async def get_doctor_bio(db: db_dependency, doctor_id: int):
    try :
        repo = DoctorInformationRepositorySQL(db)
        use_case = GetDoctorBio(repo)
        return {"Bio": use_case.execute(doctor_id=doctor_id)}
    except EntityNotFound:
        raise HTTPUserNotFound()
@router.get("/get/user-profile-picture", status_code=200)
async def get_user_profile_picture(db: db_dependency, user_id: int):
    try:
        repo = UserInformationRepositorySQL(db)
        use_case = GetUserPicture(repo)
        image_path = use_case.execute(user_id)
        return FileResponse(path=image_path, media_type="image/jpeg")
    except EntityNotFound:
        return {"there is no profile picture for this user or maybe this user dose not exist"}
@router.get("/get/user-info/get-user-basic-info", status_code=200)
async def get_user_basic_information(db: db_dependency, user: user_dependency):
    try:
        repo = UserInformationRepositorySQL(db)
        use_case = GetBasicInformation(repo)
        user_info = use_case.execute(user["id"])
        return {"f_name": user_info.f_name, "l_name": user_info.l_name, "age": user_info.age, "role": user_info.role}
    except UserNotFound:
        raise HTTPUserNotFound()

@router.post("/create-Appointments", response_model=AppointmentResponse)
@limiter.limit("5/minute")
def create_appointment(request: Request, doctor_id: int, db: db_dependency, user: dict = Depends(get_current_user)):
    try:
        repo = AppointmentRepositoryImpl(db)
        use_case = AppointmentUseCase(repo)
        appointment_entity = AppointmentEntity(
            user_id=user["id"],
            doctor_id=doctor_id,
            appointment_date=datetime.now(ZoneInfo("Asia/Amman")),
            status='pending',
            doctorname="",
            patientname=""
        )
        result = use_case.create_appointment(appointment_entity, user["id"])
        return result
    except DoctorNotAccepted:
        raise HTTPDoctorNotAccepted()
    except EntityNotFound:
        raise HTTPDoctorNotFound()

@router.get("/doctor-appointments", response_model=List[AppointmentResponse])
def get_doctor_appointments(db: db_dependency, user: dict = Depends(get_current_user)):
    try:
        validate_doctor_role(user)
        repo = AppointmentRepositoryImpl(db)
        use_case = AppointmentUseCase(repo)
        return use_case.list_appointments_for_doctor(user['id'])
    except EntityNotFound:
        raise HTTPNoAppointmentsFound

@router.put("/accept/{appointment_id}", response_model=AppointmentResponse)
def accept_appointment(appointment_id: int, db: db_dependency, user: dict = Depends(get_current_user)):
    try:
        validate_doctor_role(user)
        repo = AppointmentRepositoryImpl(db)
        use_case = AppointmentUseCase(repo)
        return use_case.accept_appointment(appointment_id,user['id'])
    except EntityNotFound:
        raise HTTPNoAppointmentsNotFound()

@router.put("/rate/doctor-rating/{doctor_id}/{rate}", status_code=201)
@limiter.limit("5/minute")
async def rate_doctor(request: Request, user: user_dependency, db: db_dependency, doctor_id: int, rate: int):
    try:
        repo = DoctorInformationRepositorySQL(db)
        use_case = RateDoctor(repo)
        use_case.execute(doctor_id, rate)
    except UnSupportedFormat:
        raise HTTPUnsupportedFileFormat()
    except UserNotFound:
        raise HTTPUserNotFound()

@router.get("/top-rated-doctors")
def get_top_rated_doctors(db: db_dependency,user: dict = Depends(get_current_user)):
    doctors =[]
    try:
        repo = DoctorRepositoryImpls(db)
        use_case = DoctorUseCase(repo)
        top_doctors = use_case.get_top_five_doctors()
        
        doctors= [
            {
                "doctor_id": doctor.Role_doctor.doctor_id,
                "rating_avg": doctor.Role_doctor.rating_avg,
                "name": doctor.f_name + " " + doctor.l_name,
                "doctor_bio":doctor.Role_doctor.bio
            }
            for doctor in top_doctors
        ]
        return doctors
    except EntityNotFound:
        raise HTTPDoctorNotFound()

@router.post("/upload-cv", status_code=201)
@limiter.limit("3/minute")
async def upload_cv(request: Request, db: db_dependency, file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    validate_doctor_role(user)
    repo = DoctorRepositoryImpl(db)
    use_case = UploadCVUseCase(repo)
    try:
        await use_case.execute(user["id"], file)
        return {'messages':'your cv uploaded successfully'}
    except UnSupportedFormat:
        raise HTTPUnsupportedFileFormat()
    except FailedToSaveFile:
        raise HTTPFailedToUploadCV()

@router.post("/report-user", status_code=201)
@limiter.limit('10/minute')
def report_users(request: Request, report_type: ReportType, description: str, reported_user_id: int, db: db_dependency, user: dict = Depends(get_current_user)):
    try:
        repo = UserReportRepositorySql(db)
        use_case = ReportUsers(repo)
        report = use_case.execute(user['id'], reported_user_id, description, report_type.name)
        return {'message': 'your report submitted successfully'}
    except EntityNotFound:
        raise HTTPUserNotFound()

@router.get("/get-patient-appointments",status_code=200)
def get_patient_appointments(request:Request,db: db_dependency, user: dict = Depends(get_current_user)):
    try:
        repo = AppointmentPatientRepoSql(db)
        use_case = AppointmentsUseCase(repo)
        return use_case.list_appointments_for_patient(user['id'])
    except EntityNotFound:
        raise HTTPNoAppointmentsFound
@router.get("/cancel-appointments",status_code=200)
def cancel_appointments(request:Request,appointment_id:int,db: db_dependency, user: dict = Depends(get_current_user)):
    try:
        repo = AppointmentPatientRepoSql(db)
        use_case = AppointmentsUseCase(repo)
        return use_case.cancel_appointments(appointment_id,user['id'])
    except EntityNotFound:
        raise HTTPNoAppointmentsFound
