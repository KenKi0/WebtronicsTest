import uuid

import fastapi

import src.models.http.post as post_http_mdl
import src.models.internal.post as post_internal_mdl
import src.core.exceptions as exc
from src.services import PostServiceProtocol, get_post_service
from src.utils.auth import Auth

router = fastapi.APIRouter(prefix='/post')


@router.post('/',
             status_code=fastapi.status.HTTP_201_CREATED,
             description='Create a post',
             tags=['Posts'])
async def create_post(
        payload: post_http_mdl.PostCreateRequest,
        service: PostServiceProtocol = fastapi.Depends(get_post_service),
        user: uuid.UUID = fastapi.Depends(Auth.login_required),
):
    await service.create_post(payload)


@router.get('/{post_id}',
            status_code=fastapi.status.HTTP_200_OK,
            description='Get a post',
            tags=['Posts'])
async def get_post(
        post_id: uuid.UUID,
        service: PostServiceProtocol = fastapi.Depends(get_post_service),
        user: uuid.UUID = fastapi.Depends(Auth.login_required)
):
    try:
        await service.get_post(post_id)
    except exc.NotFoundError:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND,
                                    detail=f'Post with id: {post_id}, doesnt exist')


@router.patch('/{post_id}',
              status_code=fastapi.status.HTTP_200_OK,
              description='Change a post',
              tags=['Posts'])
async def change_post(
        post_id: uuid.UUID,
        payload: post_http_mdl.PostUpdateRequest,
        service: PostServiceProtocol = fastapi.Depends(get_post_service),
        user: uuid.UUID = fastapi.Depends(Auth.login_required)
):
    try:
        await service.update_post(post_id, payload)
    except exc.NotFoundError:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND,
                                    detail=f'Post with id: {post_id}, doesnt exist')


@router.delete('/{post_id}',
               status_code=fastapi.status.HTTP_200_OK,
               description='Delete a post',
               tags=['Posts'])
async def delete_post(
        post_id: uuid.UUID,
        service: PostServiceProtocol = fastapi.Depends(get_post_service),
        user: uuid.UUID = fastapi.Depends(Auth.login_required)
):
    try:
        await service.delete_post(post_id)
    except exc.NotFoundError:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND,
                                    detail=f'Post with id: {post_id}, doesnt exist')


@router.post('/{post_id}/like',
             status_code=fastapi.status.HTTP_200_OK,
             description='Like a post',
             tags=['Posts'])
async def like_post(
        post_id: uuid.UUID,
        service: PostServiceProtocol = fastapi.Depends(get_post_service),
        user: uuid.UUID = fastapi.Depends(Auth.login_required)
):
    try:
        await service.rate_post(user, post_id, post_internal_mdl.PostRateEvent.like)
    except exc.NotFoundError:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND,
                                    detail=f'Post with id: {post_id}, doesnt exist')
    except exc.RateYourselfPostsError:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                                    detail='You didnt rate yourself posts')


@router.post('/{post_id}/dislike',
             status_code=fastapi.status.HTTP_200_OK,
             description='Dislike a post',
             tags=['Posts'])
async def dislike_post(
        post_id: uuid.UUID,
        service: PostServiceProtocol = fastapi.Depends(get_post_service),
        user: str = fastapi.Depends(Auth.login_required)
):
    try:
        await service.rate_post(user, post_id, post_internal_mdl.PostRateEvent.dislike)
    except exc.NotFoundError:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND,
                                    detail=f'Post with id: {post_id}, doesnt exist')
    except exc.RateYourselfPostsError:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                                    detail='You didnt rate yourself posts')
