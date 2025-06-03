from admin.repositories.get_reports import GetAllReportsRepositories


class GetReports:
    def __init__(self,repo:GetAllReportsRepositories):
        self.repo=repo
    def execute(self):
        return self.repo.get_all_reports()
class GetReportsStatus:
    def __init__(self,repo:GetAllReportsRepositories):
        self.repo=repo
    def execute(self,status:str):
        return self.repo.get_all_reports_by_status(status)