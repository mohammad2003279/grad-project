#############################################################################################################################
###### FastAPI packages #####################################################################################################
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
#############################################################################################################################
####### General packages ####################################################################################################
from typing import Annotated
from starlette import status
import asyncio
#############################################################################################################################
######## Use Cases ##########################################################################################################
from auth.use_cases.send_verification_code import SendVerificationCode#, ForgetPasswordVerificationCode
from auth.use_cases.validate_verification_code import ValidateVerificationCode
from auth.use_cases.check_user_exist import CheckUserExist, CheckUserForLogin
from auth.use_cases.accept_validation_code import AcceptCode
from auth.use_cases.generate_jwt_token import GenerateAccessToken
from auth.use_cases.refresh_token_use_case import CreateRefreshTokenUseCase, CreateAccessTokenByRefresh, Logout
#############################################################################################################################
######### Repository Implementation##########################################################################################
from auth.infrastructure.repositories.verification_request_repo_sql import VerificationRequestRepositorySQL, ForgetPasswordVCodeRepositorySQL
from auth.infrastructure.repositories.check_user_request_sql import CheckUserRequestRepositorySQL, CheckUserExistRepositorySQL
from auth.infrastructure.repositories.verification_request_accepted_sql import VerificationRequestAcceptedSQL
from auth.infrastructure.repositories.refresh_token_repository_sql import RefreshTokenRepositorySQL
#############################################################################################################################
########## Infrastructure ###################################################################################################
from infrastructure.db.dependencies import db_dependency
#############################################################################################################################
########### Dependencies ####################################################################################################
from auth.api.dependency import user_dependency
#############################################################################################################################
############ Exceptions #####################################################################################################
from core.exceptions.http_exceptions import HTTPInvalidVerificationCode, HTTPExpiredVerificationCode, HTTPUserAlreadyExist, HTTPUserNotFound, HTTPUnAuthorizedAccess, HTTPRequestNotFoundOrExpired, HTTPUserSuspended, HTTPTokenExpired, HTTPTokenNotFound
from core.exceptions.exceptions import InvalidVerificationCode, VerificationCodeExpired, UserAlreadyExist, UserNotFound, UnAuthorizedAccess, RequestNotFound, UserSuspended, TokenExpired, TokenNotFound
#############################################################################################################################






router = APIRouter(
    prefix='/auth',
    tags=['Authentication & Authorization']
)

@router.post("/send-verification-code", status_code=201)
async def send_code(email: str, db: db_dependency):
    try:
        request_repo = CheckUserRequestRepositorySQL(db)
        use_case_check_user_exist = CheckUserExist(request_repo)
        use_case_check_user_exist.execute(email.casefold())
    except UserAlreadyExist:
        raise HTTPUserAlreadyExist()
    request_repo = VerificationRequestRepositorySQL(db)
    use_case_send_verification_code = SendVerificationCode(request_repo)
    asyncio.create_task(use_case_send_verification_code.execute(email.casefold()))
    return {"Message": "Verification code sent successfully."}

@router.post("/verification-code/forget-password", status_code=201)
async def send_forget_password_code(email: str, db: db_dependency):
    try:
        request_repo = CheckUserRequestRepositorySQL(db)
        use_case_check_user_exist = CheckUserExist(request_repo)
        use_case_check_user_exist.execute(email.casefold())
        raise HTTPUserNotFound()
    except UserAlreadyExist:
        request_repo = VerificationRequestRepositorySQL(db)
        use_case = SendVerificationCode(request_repo)
        asyncio.create_task(use_case.execute(email.casefold()))
        return {"Message": "Verification code sent successfully."}



@router.post("/validate-verification-code", status_code=201)
async def validate_code(email: str, verification_code: str, db: db_dependency):
    try:
        repo = VerificationRequestRepositorySQL(db)
        use_case = ValidateVerificationCode(repo)
        use_case.execute(email.casefold(), verification_code)
        return {"Message": "Verification code has been verified."}
    except InvalidVerificationCode:
        raise HTTPInvalidVerificationCode()
    except VerificationCodeExpired:
        raise HTTPExpiredVerificationCode()
    except RequestNotFound:
        raise HTTPRequestNotFoundOrExpired()


@router.post("/token", status_code=201)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    repo_user_login = CheckUserExistRepositorySQL(db)
    use_case_user_login = CheckUserForLogin(repo_user_login)
    try:
        payload_information = use_case_user_login.execute(form_data.username, form_data.password)
    except UserNotFound: 
        raise HTTPUserNotFound() #user entered invalid password
    except UnAuthorizedAccess:
        raise HTTPUnAuthorizedAccess() #user does not exist
    except UserSuspended:
        raise HTTPUserSuspended()
    #generating the JWT token
    use_case_token_generator = GenerateAccessToken(payload_information.name, payload_information.user_id, payload_information.role)
    token = use_case_token_generator.execute()
    #generating the refresh token
    refresh_token_repo = RefreshTokenRepositorySQL(db)
    refresh_token_use_case = CreateRefreshTokenUseCase(refresh_token_repo)
    refresh_token = refresh_token_use_case.execute(payload_information.user_id)
    # returning the JWT access token and refresh token
    return {'access_token': token, 'refresh_token': refresh_token, 'token_type': 'bearer'}


@router.post("/refresh/token/", status_code=201)
async def refresh_access_token(refresh_token: str, db: db_dependency, user: user_dependency):
    try:
        repo = RefreshTokenRepositorySQL(db)
        use_case = CreateAccessTokenByRefresh(repo)
        token = use_case.execute(refresh_token)
        return token
    except TokenNotFound:
        raise HTTPTokenNotFound()
    except TokenExpired:
        raise HTTPTokenExpired()
    except UserSuspended:
        raise HTTPUserSuspended()
    

# @router.delete("/logout", status_code=201)
# async def logout(refresh_token: str, db: db_dependency):
#     try:
#         repo = RefreshTokenRepositorySQL(db)
#         use_case = Logout(repo)
#         use_case.execute(refresh_token)
#     except TokenNotFound:
#         raise HTTPTokenNotFound()