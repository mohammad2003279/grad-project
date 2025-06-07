from sqlalchemy.orm import Session
from utils.models import Test_records
from users.repositories.get_user_records_repo import ReadTestRecordsRepositories
from users.entities.user_entites import UserRecordsEntities 
from core.exceptions.exceptions import EntityNotFound

class ReadTestRecordsRepositoriesSql(ReadTestRecordsRepositories):
    def __init__(self, session: Session):
        self.session = session

    def get_records_by_userid(self, user_id: int):
        db_models = self.session.query(Test_records).filter_by(user_id=user_id).all()
        if db_models:
            return [
                UserRecordsEntities(
                    records_info={
                        'img_id': record.img_id,
                        'user_id': record.user_id,
                        'test_result': record.test_result,
                        'test_date': record.test_date
                    }
                ) for record in db_models
            ]
        else:
            raise EntityNotFound