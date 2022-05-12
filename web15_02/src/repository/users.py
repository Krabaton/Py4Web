from fastapi import status, HTTPException

from src.store.models import DbUser, db
from src.lib.hash import Hash


async def create_user(user):
    new_user = await DbUser.create(username=user.username, email=user.email, password=Hash.bcrypt(user.password))
    return new_user


async def get_users():
    users = await db.all(DbUser.query)
    return users


async def get_user(id: int):
    user = await DbUser.get(id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} not found')
    return user


async def update_user(id: int, user):
    u_user = await DbUser.get(id)
    if u_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} not found')
    await u_user.update(username=user.username, email=user.email, password=Hash.bcrypt(user.password)).apply()
    return u_user


async def delete_user(id: int):
    d_user = await DbUser.get(id)
    if d_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} not found')
    await d_user.delete()
    return d_user


async def get_user_by_username(username: str):
    user = await DbUser.query.where(DbUser.username == username).gino.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with username {username} not found')
    return user
