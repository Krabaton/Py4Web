from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from fastapi import status, HTTPException
from src.repository import users
from src.config import config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Bearer 234545345dsfdr3


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(config['auth']['expire_token']))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config['auth']['secret_key'], algorithm=config['auth']['algorithm'])
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials'
    )

    try:
        payload = jwt.decode(token, config['auth']['secret_key'], algorithms=[config['auth']['algorithm']])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await users.get_user_by_username(username)

    if user is None:
        raise credentials_exception

    return user