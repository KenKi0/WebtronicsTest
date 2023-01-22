import uuid

import fastapi

import src.core.exceptions as exc
import src.models.dto.post as post_internal_mdl
import src.models.http.post as post_http_mdl
from src.infrastructure.database.core import AsyncSession, session_provider
from src.services import IPostService, post_service_provider
from src.utils.auth import Auth

router = fastapi.APIRouter(prefix='/post')


@router.post(
    '/',
    status_code=fastapi.status.HTTP_201_CREATED,
    description='Create a post',
    tags=['Posts'],
    dependencies=[fastapi.Depends(Auth.login_required)],
)
async def create_post(
    payload: post_http_mdl.PostCreateRequest,
    service: IPostService = fastapi.Depends(post_service_provider),
    session: AsyncSession = fastapi.Depends(session_provider),
):
    await service.create_post(payload, session)


@router.get(
    '/{post_id}',
    status_code=fastapi.status.HTTP_200_OK,
    description='Get a post',
    tags=['Posts'],
    dependencies=[fastapi.Depends(Auth.login_required)],
)
async def get_post(
    post_id: uuid.UUID,
    service: IPostService = fastapi.Depends(post_service_provider),
    session: AsyncSession = fastapi.Depends(session_provider),
) -> None:
    try:
        await service.get_post(post_id, session)
    except exc.NotFoundError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=f'Post with id: {post_id}, doesnt exist'
        )


@router.patch(
    '/{post_id}',
    status_code=fastapi.status.HTTP_200_OK,
    description='Change a post',
    tags=['Posts'],
    dependencies=[fastapi.Depends(Auth.login_required)],
)
async def change_post(
    post_id: uuid.UUID,
    payload: post_http_mdl.PostUpdateRequest,
    service: IPostService = fastapi.Depends(post_service_provider),
    session: AsyncSession = fastapi.Depends(session_provider),
) -> None:
    try:
        await service.update_post(post_id, payload, session)
    except exc.NotFoundError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=f'Post with id: {post_id}, doesnt exist'
        )


@router.delete(
    '/{post_id}',
    status_code=fastapi.status.HTTP_200_OK,
    description='Delete a post',
    tags=['Posts'],
    dependencies=[fastapi.Depends(Auth.login_required)],
)
async def delete_post(
    post_id: uuid.UUID,
    service: IPostService = fastapi.Depends(post_service_provider),
    session: AsyncSession = fastapi.Depends(session_provider),
) -> None:
    try:
        await service.delete_post(post_id, session)
    except exc.NotFoundError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=f'Post with id: {post_id}, doesnt exist'
        )


@router.post(
    '/{post_id}/like',
    status_code=fastapi.status.HTTP_200_OK,
    description='Like a post',
    tags=['Posts'],
    dependencies=[fastapi.Depends(Auth.login_required)],
)
async def like_post(
    post_id: uuid.UUID,
    service: IPostService = fastapi.Depends(post_service_provider),
    session: AsyncSession = fastapi.Depends(session_provider),
    user: str = fastapi.Depends(Auth.get_user),
) -> None:
    try:
        await service.rate_post(user, post_id, post_internal_mdl.PostRateEvent.like, session)
    except exc.NotFoundError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=f'Post with id: {post_id}, doesnt exist'
        )
    except exc.RateYourselfPostsError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail='You didnt rate yourself posts'
        )


@router.post(
    '/{post_id}/dislike',
    status_code=fastapi.status.HTTP_200_OK,
    description='Dislike a post',
    tags=['Posts'],
    dependencies=[fastapi.Depends(Auth.login_required)],
)
async def dislike_post(
    post_id: uuid.UUID,
    service: IPostService = fastapi.Depends(post_service_provider),
    session: AsyncSession = fastapi.Depends(session_provider),
    user: str = fastapi.Depends(Auth.get_user),
) -> None:
    try:
        await service.rate_post(user, post_id, post_internal_mdl.PostRateEvent.dislike, session)
    except exc.NotFoundError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=f'Post with id: {post_id}, doesnt exist'
        )
    except exc.RateYourselfPostsError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail='You didnt rate yourself posts'
        )
