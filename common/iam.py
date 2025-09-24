import os
from typing import Annotated
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
from uuid import UUID

load_dotenv()

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = "HS256"

ouath2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(object):
    """
    A simple container for token payload data
    """
    def __init__(self, user_id: str, username: str | None = None, role: str | None = None):
        self.user_id = user_id
        self.username = username
        self.role = role


async def get_current_user(token: Annotated[str, Depends(ouath2_scheme)]) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id= payload.get("sub")
        role: str = payload.get("role")
        username: str = payload.get("username")
        if username is None or role is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, username=username, role=role)
    except JWTError:
        raise credentials_exception

    return token_data

def admin_required_for_method(methods: list[str]):
    async def dependency(request: Request, current_user: TokenData = Depends(get_current_user)):
        if request.method in methods:
            if current_user.role != "admin":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Admin privileges required"
                )
        return current_user
    return dependency