from services.jwt_services import AccessTokenGenerator
from enum import Enum

class DecodeAccessToken:
    def __init__(self, token):
        self.__token = token

    def execute(self):
        token = AccessTokenGenerator()
        payload = token.decode(self.__token)
        return payload