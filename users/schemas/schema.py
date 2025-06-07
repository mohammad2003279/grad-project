from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RecordsInfo(BaseModel):
    img_id:int
    user_id: Optional[int]=None
    test_result:Optional[str]=None
    test_date:Optional[datetime]=None
    