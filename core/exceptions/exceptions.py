#Core App Exceptions

class AppException(Exception):
    def __init__(self, message: str = "An application error has occurred"):
        self.message = message
        super().__init__(self.message)


class InvalidVerificationCode(AppException):
    def __init__(self):
        super().__init__("Invalid verification code.")

class RequestNotFound(AppException):
    def __init__(self):
        super().__init__("Request is not found or expired.")

class VerificationCodeExpired(AppException):
    def __init__(self):
        super().__init__("Verification code has expired")

class UserAlreadyExist(AppException):
    def __init__(self):
        super().__init__("User already exist.")

class UnAuthorizedCreateAccount(AppException):
    def __init__(self):
        super().__init__("User not verified.")

class PasswordNotMatch(AppException):
    def __init__(self):
        super().__init__("User entered wrong password")

class PasswordNewNotValid(AppException):
    def __init__(self):
        super().__init__("User used old password.")

class UnAuthorizedAccess(AppException):
    def __init__(self):
        super().__init__("User not Authorized.")

class UserNotFound(AppException):
    def __init__(self):
        super().__init__("User not found")

class UnSupportedFormat(AppException):
    def __init__(self):
        super().__init__("Unsupported file format")
        

class EntityNotFound(AppException):
    def __init__(self):
        super().__init__("Entity not found")


class FailedToSaveFile(AppException):
    def __init__(self):
        super().__init__("Failed to save file.")

class ImageNotSupported(AppException):
    def __init__(self):
        super().__init__("Image not supported for scan")


class UserSuspended(AppException):
    def __init__(self):
        super().__init__("User has been suspended")


class TokenNotFound(AppException):
    def __init__(self):
        super().__init__("Token not found.")

class TokenExpired(AppException):
    def __init__(self):
        super().__init__("Token has been expired.")

class WrongRole(AppException):
    def __init__(self):
        super().__init__("please enter a valid role")
class DoctorNotAccepted(AppException):
    def __init__(self):
        super().__init__("Doctor not accepted yet")