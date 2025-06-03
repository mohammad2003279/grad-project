from users.repositories.change_basic_information_repo import ChangeInfoRepository, ChangePasswordRepository, ChangeForgetPasswordRepository
from users.entities.user_entites import UserEntity
from passlib.context import CryptContext
from core.exceptions.exceptions import PasswordNewNotValid, PasswordNotMatch, InvalidVerificationCode, EntityNotFound

class ChangeBasicInformation:
    def __init__(self, repo: ChangeInfoRepository):
        self.repo = repo

    def execute(self, f_name, l_name, user_id):
        user = UserEntity(user_id = user_id, f_name=f_name,l_name=l_name)
        self.repo.update(user)


class ChangePassword:
    def __init__(self, repo: ChangePasswordRepository):
        self.repo = repo

    def execute(self,user_id: str, old_password: str, new_password: str):
        user = self.repo.get_by_email(user_id)
        bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        if not bcrypt_context.verify(old_password, user.hashed_password):
            raise PasswordNotMatch()
        if bcrypt_context.verify(new_password, user.hashed_password):
            raise PasswordNewNotValid()
        user.hashed_password = bcrypt_context.hash(new_password)
        self.repo.update(user)


class ForgetPassword:
    def __init__(self, repo: ChangeForgetPasswordRepository):
        self.repo = repo
    def execute(self, email: str, new_password: str):
        try:
            user = self.repo.get_by_email(email)
            bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
            if user.get("validated") == 'false':
                raise InvalidVerificationCode()
            if bcrypt_context.verify(new_password, user.get("hashed_password")):
                raise PasswordNewNotValid
            user["hashed_password"]= bcrypt_context.hash(new_password)
            user_entity = UserEntity(
                email=email,
                hashed_password=user.get("hashed_password") # type: ignore
            )
            self.repo.update(user_entity)
            self.repo.delete(email)
        except EntityNotFound:
            raise EntityNotFound() #TODO change this exception to something better