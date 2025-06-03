from auth.repositories.verification_request_repository import VerificationRequestRepository
from core.exceptions.exceptions import InvalidVerificationCode, VerificationCodeExpired, RequestNotFound, AppException
from datetime import datetime


class ValidateVerificationCode:
    def __init__(self, repo: VerificationRequestRepository):
        self.repo = repo

    def execute(self,email:str, verification_code: str):
        try:
            response = self.repo.get_by_email(email)
            v_code = response.get("v_code")
            exp = datetime.strptime(response.get("exp"), '%Y-%m-%d %H:%M:%S.%f') # type: ignore
            if response is None:
                raise RequestNotFound()
            if verification_code != v_code:
                raise InvalidVerificationCode()
            if datetime.utcnow() > exp:
                self.repo.delete(email)
                raise VerificationCodeExpired()
            self.repo.update(email)
        except RequestNotFound:
            raise RequestNotFound()