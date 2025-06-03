from auth.repositories.refresh_token_repository import RefreshTokenRepository
from auth.entities.user_entities import CheckUserExistRequest
from auth.entities.token_entity import RefreshTokenEntity
from datetime import datetime, timedelta
from utils.models import User, RefreshTokenModel
from sqlalchemy.orm import Session
from auth.schemas.refresh_token_schema import RefreshTokenSchema
from core.exceptions.exceptions import TokenNotFound


class RefreshTokenRepositorySQL(RefreshTokenRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id):
        db_model = self.session.query(User).filter_by(user_id=user_id).first()
        return CheckUserExistRequest(
            user_id = db_model.user_id,
            hashed_password="",
            f_name=db_model.f_name,
            l_name=db_model.l_name,
            role= db_model.role,
            suspended=db_model.suspension
        )
    
    def add(self, token: str, expires_at: datetime, user_id: int):
        db_model = RefreshTokenModel(
            jwt_token = token,
            user_id = user_id,
            created_at = datetime.utcnow(),
            expires_at = expires_at,
            revoked = False
        )
        self.session.add(db_model)
        self.session.commit()

    def get_by_token(self, token):
        db_model = self.session.query(RefreshTokenModel).filter_by(jwt_token=token).first()
        if db_model is None:
            raise TokenNotFound()
        return RefreshTokenEntity(
            token = db_model.jwt_token,
            user_id = db_model.user_id,
            expires_at=db_model.expires_at,
            revoked=db_model.revoked
        )
    

    def delete(self, token: str):
        self.session.query(RefreshTokenModel).filter_by(jwt_token=token).delete()
        self.session.commit()


    def update(self, old_token: str, new_token: str):
        db_model = self.session.query(RefreshTokenModel).filter_by(jwt_token=old_token).first()
        db_model.jwt_token = new_token
        db_model.created_at = datetime.utcnow()
        db_model.expires_at = datetime.utcnow() + timedelta(days=7)
        self.session.commit()
        self.session.refresh(db_model)