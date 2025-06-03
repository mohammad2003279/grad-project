from users.repositories.reports import UserReportRepository
from sqlalchemy.orm import Session
from utils.models import User, ReportHistory
from users.entities.user_entites import ReportEntity
from datetime import datetime
from zoneinfo import ZoneInfo
from core.exceptions.exceptions import EntityNotFound


class UserReportRepositorySql(UserReportRepository):
    def __init__(self, session: Session):
        self.session = session

    def report_user(self, user_id: int, user_reported: int, description: str, report_type: str):
        reporter = self.session.query(User).filter_by(user_id = user_id).first()
        reported = self.session.query(User).filter_by(user_id = user_reported).first()
        if not reporter or not reported:
            raise EntityNotFound

        report_db = ReportHistory(
            reporter_id=user_id,
            reported_user_id=user_reported,
            description=description,
            status='pending',
            created_at=datetime.now(ZoneInfo("Asia/Amman")),
            report_type=report_type,
            updated_at=datetime.now(ZoneInfo("Asia/Amman"))
        )

        self.session.add(report_db)
        self.session.commit()
