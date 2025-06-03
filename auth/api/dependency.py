from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from auth.services.jwt_services import AccessTokenGenerator
from core.exceptions.http_exceptions import HTTPUnAuthorizedAccess, HTTPUserNotFound
from typing import Annotated
from datetime import datetime
from jose import JWTError


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")



async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = AccessTokenGenerator().decode(token) #decode the jwt
        #get the user info from the jwt token
        name = payload.get("sub")
        user_id = payload.get("id")
        role = payload.get("role")
        exp = payload.get("exp")
        if name is None or user_id is None:
            raise HTTPUserNotFound()
        return {"sub": name, "id": user_id, "role": role, "exp": exp}
    except JWTError:
        raise HTTPUnAuthorizedAccess()

user_dependency = Annotated[dict, Depends(get_current_user)]