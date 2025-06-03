from users.repositories.check_user_validated_code import CheckUserValidatedCode
from core.exceptions.exceptions import UnAuthorizedCreateAccount, RequestNotFound

class CheckAccountValidation:
    def __init__(self, repo: CheckUserValidatedCode):
        self.repo = repo

    def execute(self, email: str):
        try:
            status = self.repo.get_by_email(email)
            if status.get("validated") == 'false':
                raise UnAuthorizedCreateAccount()
            self.repo.delete(email)
        except RequestNotFound:
            raise UnAuthorizedCreateAccount()