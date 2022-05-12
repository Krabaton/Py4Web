from fastapi import APIRouter, Response, status, Depends
from typing import Optional, List
from src.schemas.users import UserModel, UserResponse

from src.repository import users

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/', response_model=List[UserResponse])
async def get_users():
    all_users = await users.get_users()
    return all_users


@router.get('/{id}', response_model=UserResponse)
async def get_comment(id: int):
    user = await users.get_user(id)
    return user


@router.post('/', response_model=UserResponse)
async def create_user(user: UserModel):
    new_user = await users.create_user(user)
    return new_user.to_dict()


@router.put('/{id}', response_model=UserResponse)
async def update_user(user: UserModel, id: int):
    up_user = await users.update_user(id, user)
    return up_user.to_dict()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int):
    up_user = await users.delete_user(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
