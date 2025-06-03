from auth.repositories.refresh_token_repository import RefreshTokenRepository
from auth.services.jwt_services import RefreshTokenGenerator, AccessTokenGenerator
from datetime import timedelta, datetime
from core.exceptions.exceptions import TokenNotFound, TokenExpired, UserSuspended, AppException


class CreateRefreshTokenUseCase:
    def __init__(self, repo: RefreshTokenRepository):
        self.repo = repo

    def execute(self, user_id: int):
        Encoder = RefreshTokenGenerator()
        auth_user_entity = self.repo.get_by_id(user_id)
        payload = {"name": auth_user_entity.name}
        refresh_token= Encoder.encode(payload)
        self.repo.add(refresh_token, datetime.utcnow() + timedelta(days=7), auth_user_entity.user_id)
        return refresh_token
    

class CreateAccessTokenByRefresh:
    def __init__(self, repo: RefreshTokenRepository):
        self.repo = repo

    def execute(self, token: str):
        try:
            token_validation = self.repo.get_by_token(token)
            if token_validation.is_expired():
                self.repo.delete(token)
                raise TokenExpired()
            if token_validation.is_revoked():
                self.repo.delete(token)
                raise UserSuspended()
            user_information = self.repo.get_by_id(token_validation.user_id)
            access_token_payload = {"name": user_information.name, "user_id": user_information.user_id, "role": user_information.role}
            refresh_token_payload = {"name": user_information.name}
            access_token_generator = AccessTokenGenerator()
            refresh_token_generator = RefreshTokenGenerator()
            access_token = access_token_generator.encode(access_token_payload)
            refresh_token = refresh_token_generator.encode(refresh_token_payload)
            self.repo.update(token, refresh_token)
            return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}
        except TokenNotFound:
            raise TokenNotFound()
        

class Logout:
    def __init__(self, repo: RefreshTokenRepository):
        self.repo = repo

    def execute(self, token: str):
        try:
            self.repo.delete(token)
        except Exception:
            raise TokenNotFound()