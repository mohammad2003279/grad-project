import random, string
from auth.entities.verification_request import VerificationRequest
from auth.repositories.verification_request_repository import VerificationRequestRepository
from auth.services.notification_services import Mail
from datetime import datetime, timedelta
from fastapi import BackgroundTasks
from core.exceptions.exceptions import UserAlreadyExist, AppException, UserNotFound
import redis
import json


class SendVerificationCode:
    def __init__(self, request_repo: VerificationRequestRepository):
        self.request_repo = request_repo

    async def execute(self, email: str, length=6):

        verification_code = ''.join(random.choices(string.digits, k = length))
        expiration = datetime.utcnow() + timedelta(minutes=15)
        request_entity = VerificationRequest(email, verification_code, expiration)
        status = self.request_repo.add(request_entity)


        #send the verification code via email
        verification_mail = Mail()
        status = await verification_mail.send_mail(email, verification_code)
        return status


# class ForgetPasswordVerificationCode:
#     def __init__(self, repo: VerificationRequestRepository):
#         self.repo = repo

#     async def execute(self, email: str, length=6):
#         verification_code = ''.join(random.choices(string.digits, k = length))
#         expiration = datetime.utcnow() + timedelta(minutes=15)
#         request = VerificationRequest(email, verification_code, expiration)
#         self.repo.add(request)
#         request = {"v_code": verification_code, "expiration": expiration, "validated": False}
#         cache_key = f"UserEmail:{email}"
#         verification_mail = Mail()
#         await verification_mail.send_mail(email, verification_code)
