from scan.repositories.scan_image_repository import ScanImageRepository
from sqlalchemy.orm import Session
from scan.entities.test_record_entity import TestRecordEntity
from utils.models import Test_records
#from scan.schemas.test_records_schema import TestRecordSchema
from datetime import datetime

class ScanImageRepositorySQL(ScanImageRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, request: TestRecordEntity):
        db_model = Test_records(
            img_path = request.img_name,
            user_id = request.user_id,
            test_result = request.test_result,
            test_date = datetime.utcnow(),
            test_ratio = request.test_ratio
        )
        self.session.add(db_model)
        self.session.commit()
        
    def update(self, user_id: int):
        db_model = self.session.query(Test_records).filter_by(user_id=user_id).first()
        image_name = str(db_model.img_id)
        img_ext = db_model.img_path.split(".")[-1]
        file_name = f"{image_name}.{img_ext}"
        db_model.img_path = file_name
        self.session.commit()
        self.session.refresh(db_model)