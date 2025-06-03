from admin.repositories.get_reports import GetAllReportsRepositories
from sqlalchemy.orm import Session
from utils.models import ReportHistory

class GetAllReportsSql(GetAllReportsRepositories):
    def __init__(self,session:Session):
        self.session=session
    def get_all_reports(self):
        model_db=self.session.query(ReportHistory).all()

        return [
            {
                "report_id":report.id,
                "reporter_id":report.reporter_id,
                "reported_user_id":report.reported_user_id,
                "report_type":report.report_type,
                "description":report.description,
                "status":report.status,
                "created_at":report.created_at
            }
            for report in model_db
        ]
    def get_all_reports_by_status(self,status:str):
        model_db = self.session.query(ReportHistory).filter_by(status=status).all()
        return [
            {
                "report_id":report.id,
                "reporter_id":report.reporter_id,
                "reported_user_id":report.reported_user_id,
                "report_type":report.report_type,
                "description":report.description,
                "status":report.status,
                "created_at":report.created_at
            }
            for report in model_db
        ]