from fastapi import APIRouter, status, HTTPException
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from src.repository import users
from src.store.models import db, DbUser
from src.lib.hash import Hash
from src.lib import oauth2


router = APIRouter(
    tags=['auth']
)


@router.post('/token')
async def get_token(request: OAuth2PasswordRequestForm = Depends()):
    user = await users.get_user_by_username(request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")

    access_token = oauth2.create_access_token(data={'sub': user.username})

    return {
        'access_token': access_token,
        'token_type': 'Bearer',
        'user_id': user.id,
        'username': user.username
    }
