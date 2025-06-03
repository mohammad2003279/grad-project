from admin.repositories.remove_records import RemoveTestRecordsRepositories


class RemoveRecordsByImageId:
    def __init__(self,repo:RemoveTestRecordsRepositories):
        self.repo=repo
    def execute(self,img_id:int):
        self.repo.removeRecords(img_id)


