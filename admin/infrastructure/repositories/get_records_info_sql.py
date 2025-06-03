from sqlalchemy.orm import Session
from utils.models import Test_records
from admin.repositories.get_records_info import ReadTestRecordsRepositories
from admin.entities.admin_entities import AdminRecordsEntities 
from core.exceptions.exceptions import EntityNotFound

class ReadTestRecordsRepositoriesSql(ReadTestRecordsRepositories):
    def __init__(self, session: Session):
        self.session = session

    def get_all_test_records(self):
        db_models = self.session.query(Test_records).all()

        if db_models:

            return [
                AdminRecordsEntities(
                    records_info={
                        'img_id': record.img_id,
                        'user_id': record.user_id,
                        'test_result': record.test_result,
                        'test_date': record.test_date
                    }
                ) for record in db_models
            ]
        else : 
            raise EntityNotFound

    def get_records_by_userid(self, user_id: int):
        db_models = self.session.query(Test_records).filter_by(user_id=user_id).all()
        if db_models:
            return [
                AdminRecordsEntities(
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

    def get_record_by_img_id(self, img_id: int):
        db_model = self.session.query(Test_records).filter_by(img_id=img_id).first()
        if db_model:
            return AdminRecordsEntities(
                records_info={
                    'img_id': db_model.img_id,
                    'user_id': db_model.user_id,
                    'test_result': db_model.test_result,
                    'test_date': db_model.test_date
                }
            )
        else :
            raise EntityNotFound
