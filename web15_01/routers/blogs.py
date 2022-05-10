from fastapi import APIRouter, status, Response, Query, Path
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field

router = APIRouter(
    prefix='/blogs',
    tags=['blogs']
)


class BlogType(str, Enum):
    all = 'all'
    politics = 'politics'
    beauty = 'beauty'
    sports = 'sports'


@router.get('/')
def get_blogs(type: BlogType = 'all',
              limit: int = Query(10, ge=10, title='Limit blogs', description='How we want to get blogs'),
              offset: Optional[int] = 0):
    return {'message': f'All {limit} blogs {offset}'}


@router.get('/{blogId}', status_code=status.HTTP_200_OK)
def get_blogs(response: Response, blogId: int = Path(..., ge=1)):
    # if blogId == 0:
    #     response.status_code = status.HTTP_400_BAD_REQUEST
    #     return {'message': f'Blog not exist for id = {blogId}'}
    return {'message': f'Get {blogId} blog'}


@router.get('/{blogId}/comments', status_code=status.HTTP_200_OK, tags=['comments'])
def get_blogs(blogId: int, response: Response):
    """
    - :param **blogId**: Номер блога
    - :return: Всі коменти під цим блогом
    """
    if blogId == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': f'Blog not exist for id = {blogId}'}
    return {'message': f'Get comments for {blogId} blog'}


@router.get('/type/{type}')
def get_blogs_of_type(type: BlogType):
    return {'message': f'Type: {type}'}


class Picture(BaseModel):
    urls: List[str] = None


class BlogModel(BaseModel):
    title: str = Field(min_length=5)
    price: int = Field(gt=1)
    body: str
    tags: List[str] = []
    pictures: Optional[Picture] = None


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(blog: BlogModel):
    return {
        'blog': blog
    }
