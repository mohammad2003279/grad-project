from core.exceptions.http_exceptions import HTTPUnAuthorizedUser

def validate_doctor_role(user: dict):
    if user.get("role", "").lower() != "doctor":
        raise HTTPUnAuthorizedUser()