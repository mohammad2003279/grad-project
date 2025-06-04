from users.repositories.get_most_avg_rate import DoctorRepository
from utils.models import Role_doctor, User
from sqlalchemy.orm import Session
from core.exceptions.exceptions import EntityNotFound
class DoctorRepositoryImpls(DoctorRepository):
    def __init__(self, session: Session):
        self.session = session
    def get_top_rated_doctors(self, limit: int = 5):
        result = (
            self.session.query(Role_doctor, User.f_name, User.l_name)
            .join(User, Role_doctor.doctor_id == User.user_id)
            .filter(Role_doctor.rating_avg != None, Role_doctor.accepted == True)
            .order_by(Role_doctor.rating_avg.desc())
            .limit(limit)
            .all()
        )
        if not result:
            raise EntityNotFound
        return result
