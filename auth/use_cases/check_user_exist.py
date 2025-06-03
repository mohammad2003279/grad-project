from auth.entities.user_entities import CheckUserRequest, CheckUserExistRequest
from auth.repositories.check_user_request_repository import CheckUserRequestRepository, CheckUserExistRepository
from core.exceptions.exceptions import UserAlreadyExist, UserNotFound, UnAuthorizedAccess, UserSuspended
from passlib.context import CryptContext

class CheckUserExist:
    def __init__(self, repo: CheckUserRequestRepository):
        self.repo = repo

    def execute(self, email: str):
        if self.repo.get_by_email(email):
            raise UserAlreadyExist()

class CheckUserForLogin:
    def __init__(self, repo: CheckUserExistRepository):
        self.repo = repo

    def execute(self, email, password):
        try:
            repo_response = self.repo.get_by_email(email)
            bycript_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
            if not bycript_context.verify(password, repo_response.hashed_password):
                raise UnAuthorizedAccess() #raise Exception for invalid password
            if repo_response.suspended:
                raise UserSuspended()
        except UnAuthorizedAccess:
            raise UnAuthorizedAccess() #raise Exception for user does not exist
        return repo_response