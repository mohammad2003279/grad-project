from fastapi import HTTPException
from starlette import status

class HTTPInvalidVerificationCode(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your verification code is invalid."
        )

class HTTPRequestNotFoundOrExpired(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Your Request is not supported or expired."
        )

class HTTPExpiredVerificationCode(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your verification code has expired."
        )

class HTTPUserAlreadyExist(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exist."
        )

class HTTPUnAuthorizedCreateAccount(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please verify your verification code first."
        )

class HTTPPassswordNotMatch(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Wrong password"
        )

class HTTPPasswordNewNotValid(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="New password can't be same as new password"
        )


class HTTPUnAuthorizedAccess(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Your email or password is invalied."
        )

class HTTPUserNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User does not exist."
        )

class HTTPUnAuthorizedUser(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Your are not allowed to perform this operation."
        )

class HTTPUnsupportedFileFormat(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = "File format is not supported."
        )

class HTTPFailedToUploadPicture(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_501_NOT_IMPLEMENTED,
            detail = "Failed to upload your profile picture, please try again later"
        )

class HTTPFailedToUploadCV(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail = "Failed to upload your CV, please try again later"
        )

class HTTPFailedToFetchImage(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_501_NOT_IMPLEMENTED,
            detail = "Failed to fetch profile picture."
        )

class HTTPImageNotSupported(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = "Your image is not dermoscopic skin image.please try different type or report the error."
        )


class HTTPUserSuspended(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your account has been suspended, plese review your email or contact our support team."
        )


class HTTPTokenNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Your refresh token could not be found."
        )


class HTTPTokenExpired(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Your refresh token has expired, please re-login again."
        )

class HTTPWrongRole(HTTPException):
    def __init__(self):
        super().__init__(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="please enter a valid role"
        )
class HTTPRecordNotFound(HTTPException):
    def __init__(self):
        super().__init__(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Record Not Found"
        )
class HTTPRecordIsEmpty(HTTPException):
    def __init__(self):
        super().__init__(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No records yet"
        )
class HTTPDoctorNotAccepted(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Doctor not accepted yet"
        )
class HTTPDoctorNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No doctor found"
        )
class HTTPNoAppointmentsFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no appoitments yet "
        )
class HTTPNoAppointmentsNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no appointment at this ID"
        )