from datetime import datetime


class CheckUserRequest:
    def __init__(self, email):
        self.email = email

    def does_user_exist(self, email):
        if self.email == email:
            return True

class CheckUserExistRequest:
    def __init__(self,user_id: int, hashed_password: str, f_name: str, l_name: str, role: str, suspended: bool):
        self.user_id = user_id
        self.hashed_password = hashed_password
        self.name = f_name + ' ' + l_name
        self.role = role
        self.suspended = suspended