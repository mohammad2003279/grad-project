from sqlalchemy.orm import Session
from utils.models import Test_records
from admin.repositories.remove_records import RemoveTestRecordsRepositories
from core.exceptions.exceptions import EntityNotFound

class RemoveTestRecordsRepositoriesSql(RemoveTestRecordsRepositories):
    def __init__(self, session: Session):
        self.session = session

    def removeRecords(self, img_id: int):
        db_model = self.session.query(Test_records).filter_by(img_id=img_id).first()
        if db_model:
            self.session.delete(db_model)
            self.session.commit()
        else:
            raise EntityNotFound
