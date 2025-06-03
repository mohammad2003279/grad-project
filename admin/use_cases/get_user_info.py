from admin.repositories.get_user_info import ReadUsersInfoRepositories
from core.exceptions.exceptions import EntityNotFound, WrongRole
from admin.entities.admin_entities import AdminUserEntities

class GetUserInfoById:
    def __init__(self,repo:ReadUsersInfoRepositories):
        self.repo = repo
    
    def execute(self,user_id:int):
        return self.repo.get_by_id(user_id)

class GetUserInfoByRole:
    def __init__(self,repo:ReadUsersInfoRepositories):
        self.repo=repo
        
    def execute(self,role:str):
        try:
            response = self.repo.get_by_role(role)
            users = []
            for user in response: # type: ignore
                users.append(AdminUserEntities( #type: ignore
                    user_id = user.user_id,
                    email = user.email,
                    name = user.f_name + ' ' + user.l_name,
                    role = user.role,
                    signup_date=user.signup_date,
                    suspension=user.suspension
                ))
            return users
        except WrongRole:
            raise WrongRole()


class GetAllUsersInfo:
    def __init__(self,repo:ReadUsersInfoRepositories):
        self.repo=repo
        
    def execute(self,):
        return self.repo.get_all_users_info()