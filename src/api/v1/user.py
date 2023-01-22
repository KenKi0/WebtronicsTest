import uuid
from dataclasses import asdict

import fastapi

import src.core.exceptions as exc
import src.models.http.post as post_http_mdl
import src.models.http.user as user_http_mdl
from src.infrastructure.database.core import AsyncSession, session_provider
from src.services import IUserService, user_service_provider
from src.utils.auth import Auth

router = fastapi.APIRouter(prefix='/user')


@router.get(
    '/{user_id}/posts',
    response_model=list[post_http_mdl.PostResponse],
    status_code=fastapi.status.HTTP_201_CREATED,
    description='Get user posts',
    tags=['Users'],
    dependencies=[fastapi.Depends(Auth.login_required)],
)
async def get_user_posts(
    user_id: uuid.UUID,
    service: IUserService = fastapi.Depends(user_service_provider),
    session: AsyncSession = fastapi.Depends(session_provider),
) -> list[post_http_mdl.PostResponse]:
    posts = await service.get_user_posts(user_id, session)
    return [post_http_mdl.PostResponse.parse_obj(asdict(post)) for post in posts]


@router.patch(
    '/{user_id}',
    status_code=fastapi.status.HTTP_201_CREATED,
    description='Change a user info',
    tags=['Users'],
    dependencies=[fastapi.Depends(Auth.login_required)],
)
async def change_user_info(
    user_id: uuid.UUID,
    payload: user_http_mdl.UserUpdateRequest,
    service: IUserService = fastapi.Depends(user_service_provider),
    session: AsyncSession = fastapi.Depends(session_provider),
) -> None:
    try:
        await service.update_user_info(user_id, payload, session)
    except exc.NotFoundError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=f'User with id: {user_id}, doesnt exist'
        )
    except exc.UniqueFieldError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail='User with specified fields already exist'
        )
