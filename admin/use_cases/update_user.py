from admin.repositories.update_user import SuspensionUserRepositories,AcceptionDoctorRepositories


class Suspension:
    def __init__(self,repo:SuspensionUserRepositories):
        self.repo=repo
    def execute(self,user_id:int):
        return self.repo.suspensionUser(user_id)

class Acception:
    def __init__(self,repo:AcceptionDoctorRepositories):
        self.repo=repo
    def execute(self,doctor_id:int):
        return self.repo.acceptionDoctor(doctor_id)
        