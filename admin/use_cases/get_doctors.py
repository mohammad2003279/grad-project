from admin.repositories.get_doctors_by_acception import GetDoctorsByAcception
from admin.entities.admin_entities import AdminDoctorEntities


class GetDoctors:
    def __init__(self,repo:GetDoctorsByAcception):
        self.repo = repo
    def execute(self,acception:bool) -> list[AdminDoctorEntities]:
        return self.repo.get_doctors_by_acception(acception)


