from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
from jose import jwt, JWTError
from fastapi import HTTPException
import uuid
from core.exceptions.exceptions import UserNotFound

load_dotenv()

class AccessTokenGenerator:
    def __init__(self):
        # self.__SECRET_KEY = str(os.getenv("SECRET_KEY"))
        # self.__ALGORITHM = str(os.getenv("ALGORITHM"))
        self.__SECRET_KEY="197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3"
        self.__ALGORITHM="HS256"

    def encode(self, payload, duration: timedelta = timedelta(minutes=30)):
        expire_date = datetime.utcnow() + duration
        encode = {'sub': payload.get('name'), 'id': payload.get('user_id'), 'role': payload.get('role'), 'exp': expire_date}
        return jwt.encode(encode, self.__SECRET_KEY, algorithm=self.__ALGORITHM)

    def decode(self, token):
        try:
            payload = jwt.decode(token, self.__SECRET_KEY, algorithms=self.__ALGORITHM)
            name: str = payload.get('sub') # type: ignore
            user_id: int = payload.get('id') # type: ignore
            user_role: str = payload.get('role') # type: ignore
            expiration: datetime = payload.get('exp') # type: ignore
            if name is None or user_id is None:
                    return False
            return {'sub': name, 'id': user_id, 'role': user_role, 'exp': expiration}
        except JWTError:
            raise HTTPException(status_code=404, detail=f"an error occurred : {JWTError}")
        


class RefreshTokenGenerator:
    def __init__(self):
        self.__SECRET_KEY="197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3"
        self.__ALGORITHM="HS256"
        #self.__SECRET_KEY = str(os.getenv("SECRET_KEY"))
        #self.__ALGORITHM = str(os.getenv("ALGORITHM"))

    def encode(self, payload, duration: timedelta = timedelta(days=7)):
        expire_date = datetime.utcnow() + duration
        encode = {"sub": payload.get("name"), "exp": expire_date, "jti": str(uuid.uuid4())}
        return jwt.encode(encode, self.__SECRET_KEY, algorithm=self.__ALGORITHM)
    
    def decode(self, token):
        try:
            payload = jwt.decode(token, self.__SECRET_KEY, algorithms=self.__ALGORITHM)
            name = payload.get("sub")
            exp = payload.get("exp")
            jti = payload.get("jti")
            if name is None or jti is None:
                raise UserNotFound()
            return {"sub": name, "exp": exp, "jti": jti}
        except JWTError:
            raise HTTPException(status_code=404, detail=f"an error occurred : {JWTError}")