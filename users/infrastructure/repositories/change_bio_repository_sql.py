from users.repositories.change_bio_repository import ChangeBioRepository
from sqlalchemy.orm import Session
from utils.models import Role_doctor, User
from users.entities.user_entites import UserEntity

class ChangeBioRepositorySQL(ChangeBioRepository):
    def __init__(self, session: Session):
        self.session = session
        
    def get_by_email(self, user_id: int):
        db_model = self.session.query(User).filter_by(user_id=user_id).first()
        return UserEntity(
            user_id = db_model.user_id,
            role = db_model.role
        )
        
    def update(self, bio: str, user_id: int):
        db_model = self.session.query(Role_doctor).filter_by(doctor_id=user_id).first()
        db_model.bio = bio
        self.session.commit()
        self.session.refresh(db_model)