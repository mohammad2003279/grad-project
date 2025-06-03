from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.orm import Session
from infrastructure.db.dependencies import db_dependency
from users.api.dependencies import user_dependency
from admin.infrastructure.repositories.get_user_info_sql import ReadUsersInfoRepositoriesSql 
from admin.use_cases.get_user_info import GetUserInfoById, GetUserInfoByRole ,GetAllUsersInfo
from core.exceptions.exceptions import EntityNotFound,WrongRole
from admin.infrastructure.repositories.remove_records_sql import RemoveTestRecordsRepositoriesSql
from admin.use_cases.remove_records import RemoveRecordsByImageId
from admin.use_cases.get_all_reports_usecase import GetReports,GetReportsStatus
from admin.infrastructure.repositories.get_records_info_sql import ReadTestRecordsRepositoriesSql
from admin.use_cases.get_records_info import GetAllRecords,GetRecordsByUserId,GetRecordsByImageId
from utils.report_type import StatusType
from admin.infrastructure.repositories.update_user_sql import SuspensionUserRepositoriesSql, AcceptionDoctorRepositoriesSql
from admin.infrastructure.repositories.get_reports_sql import GetAllReportsSql
from admin.use_cases.update_user import Suspension, Acception

from auth.api.dependency import get_current_user

from core.exceptions.http_exceptions import HTTPRecordIsEmpty,HTTPUnAuthorizedUser,HTTPUserNotFound,HTTPWrongRole,HTTPRecordNotFound

from fastapi import APIRouter, status

from admin.use_cases.validate_admin import validate_admin_role

from admin.infrastructure.repositories.get_doctors_by_acception_sql import GetDoctorsByAcceptionRepo
from admin.use_cases.get_doctors import GetDoctors

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

@router.get("/info/{user_id}",status_code=status.HTTP_200_OK)
def get_user_info_by_id(user_id: int, db: db_dependency, user: dict = Depends(get_current_user)):
    try:
        validate_admin_role(user["role"])
        repo = ReadUsersInfoRepositoriesSql(db)
        usecase = GetUserInfoById(repo)
    
        return usecase.execute(user_id)
    except EntityNotFound :
        raise HTTPUserNotFound

@router.get("/all-users-info",status_code=status.HTTP_200_OK)
def get_all_users_info(db: db_dependency, user: dict = Depends(get_current_user)):
    try:
        validate_admin_role(user["role"])
        repo = ReadUsersInfoRepositoriesSql(db)
        usecase = GetAllUsersInfo(repo)
    
        return usecase.execute()
    except EntityNotFound :
        raise HTTPUserNotFound
        
@router.get("/role/{role}")
def get_user_info_by_role(role: str, db: db_dependency, user: dict = Depends(get_current_user)):
    validate_admin_role(user["role"])
    try:
        repo = ReadUsersInfoRepositoriesSql(db)
        use_case = GetUserInfoByRole(repo)
        return use_case.execute(role)
    except EntityNotFound :
        raise HTTPUserNotFound
    except WrongRole:
        raise HTTPWrongRole

@router.delete("/remove/{img_id}",status_code=status.HTTP_200_OK)
def remove_record_by_img_id(img_id: int, db: db_dependency, user: dict = Depends(get_current_user)):
    try:
        validate_admin_role(user["role"])
        repo = RemoveTestRecordsRepositoriesSql(db)
        usecase = RemoveRecordsByImageId(repo)
        usecase.execute(img_id)
        return {"message":"record deleted successfully"}
    except EntityNotFound:
        raise HTTPRecordNotFound
@router.get("/get-all-records")
def get_all_records(db: db_dependency, user: dict = Depends(get_current_user)):
    validate_admin_role(user["role"])
    try:
        repo=ReadTestRecordsRepositoriesSql(db)
        usecase = GetAllRecords(repo)
        return usecase.execute()
    except EntityNotFound:
        raise HTTPRecordIsEmpty

@router.get("/user/record/{user_id}")
def get_records_by_user_id(user_id: int, db: db_dependency, user: dict = Depends(get_current_user)):
    validate_admin_role(user["role"])
    try:
        usecase = GetRecordsByUserId(repo=ReadTestRecordsRepositoriesSql(db))
        return usecase.execute(user_id)
    except:
        raise HTTPRecordNotFound

@router.get("/image/{img_id}")
def get_record_by_image_id(img_id: int, db: db_dependency, user: dict = Depends(get_current_user)):
    try:
        validate_admin_role(user["role"])
        usecase = GetRecordsByImageId(repo=ReadTestRecordsRepositoriesSql(db))
        return usecase.execute(img_id)
    except EntityNotFound:
        raise HTTPRecordNotFound

@router.put("/user/suspend/{user_id}")
def suspend_user(user_id: int, db: db_dependency, user: dict = Depends(get_current_user)):
    validate_admin_role(user["role"])
    repo = SuspensionUserRepositoriesSql(db)
    usecase = Suspension(repo)
    try:
        return usecase.execute(user_id)
    except EntityNotFound:
        raise HTTPUserNotFound

@router.put("/doctor/accept/{doctor_id}")
def accept_doctor(doctor_id: int, db: db_dependency, user: dict = Depends(get_current_user)):
    try:
        validate_admin_role(user["role"])
        repo = AcceptionDoctorRepositoriesSql(db)
        usecase = Acception(repo)
        return usecase.execute(doctor_id)
    except EntityNotFound:
        raise HTTPUserNotFound

@router.get("/not-accepted-doctor")
def get_doctors_by_acception(acception: bool,db:db_dependency,user:dict=Depends(get_current_user)):
    validate_admin_role(user["role"])
    repo = GetDoctorsByAcceptionRepo(db)
    use_case = GetDoctors(repo)
    return use_case.execute(acception)

@router.get("/get-reports-by-status")
def get_reports(status:StatusType ,db:db_dependency,user:dict=Depends(get_current_user)):
    validate_admin_role(user["role"])
    repo=GetAllReportsSql(db)
    use_case=GetReportsStatus(repo)
    return use_case.execute(status.name)