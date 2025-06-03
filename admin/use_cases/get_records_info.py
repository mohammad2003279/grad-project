from admin.repositories.get_records_info import ReadTestRecordsRepositories
from core.exceptions.exceptions import EntityNotFound

class GetAllRecords:
    def __init__(self,repo:ReadTestRecordsRepositories):
        self.repo=repo
    def execute(self):
        return self.repo.get_all_test_records()




class GetRecordsByUserId:
    def __init__(self,repo:ReadTestRecordsRepositories):
        self.repo=repo
    def execute(self,user_id:int):
        return self.repo.get_records_by_userid(user_id)


class GetRecordsByImageId:
    def __init__(self,repo:ReadTestRecordsRepositories):
        self.repo=repo
    def execute(self,img_id:int):
        return self.repo.get_record_by_img_id(img_id)