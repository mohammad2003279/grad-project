from users.repositories.get_user_records_repo import ReadTestRecordsRepositories
from core.exceptions.exceptions import EntityNotFound


class GetRecordsByUserId:
    def __init__(self,repo:ReadTestRecordsRepositories):
        self.repo=repo
    def execute(self,user_id:int):
        return self.repo.get_records_by_userid(user_id)
