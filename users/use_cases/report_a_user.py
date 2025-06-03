from users.repositories.reports import UserReportRepository


class ReportUsers:
    def __init__(self,repo:UserReportRepository):
        self.repo=repo
    def execute(
        self,
        user_id: int,
        user_reported: int,
        description: str,
        report_type: str
    ):
        return self.repo.report_user(user_id, user_reported, description, report_type)
