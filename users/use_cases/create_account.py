from users.repositories.create_account_request_repository import CreateAccountRequestRepository, CreateDoctorAccountRepository
from utils.models import User
from users.schemas.create_account_schema import CreateAccountSchema
from passlib.context import CryptContext

class CreateAccountRequest:
    def __init__(self, user_repo: CreateAccountRequestRepository, doctor_repo: CreateDoctorAccountRepository = None): # type: ignore
        self.user_repo = user_repo
        self.doctor_repo = doctor_repo

    def execute(self, cam: CreateAccountSchema): #cam stands for create account schema
        cam.role = cam.role.casefold()
        cam.email = cam.email.casefold()
        cam.sex = cam.sex.casefold()
        bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        cam.hashed_password = bcrypt_context.hash(cam.hashed_password)
        self.user_repo.add(cam)
        if cam.role == 'doctor':
            self.doctor_repo.add(cam.email)
