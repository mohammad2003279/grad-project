from core.exceptions.http_exceptions import HTTPUnAuthorizedUser

def validate_admin_role(role: str):
    if role.casefold() != 'admin':
        raise HTTPUnAuthorizedUser()