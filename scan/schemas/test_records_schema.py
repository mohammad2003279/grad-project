from pydantic import BaseModel
from datetime import datetime

class TestRecordSchema(BaseModel):
    img_path: str
    user_id: int
    test_result: str
    test_date: datetime