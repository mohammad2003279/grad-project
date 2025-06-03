from fastapi import Depends
from typing import Annotated
from infrastructure.db.db_injection import get_db
from sqlalchemy.orm import Session

db_dependency = Annotated[Session, Depends(get_db)]
