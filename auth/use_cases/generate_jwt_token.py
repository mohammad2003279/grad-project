from auth.services.jwt_services import AccessTokenGenerator

class GenerateAccessToken:
    def __init__(self, name: str, user_id: int, role: str):
        self.__name = name
        self.__user_id = user_id
        self.__role = role

    def execute(self):
        payload = {'name': self.__name, 'user_id': self.__user_id, 'role': self.__role}
        token = AccessTokenGenerator()
        return token.encode(payload)
