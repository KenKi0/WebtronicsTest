import uuid
from dataclasses import asdict

import fastapi

import src.core.exceptions as domain_exc
import src.api.exceptions.exceptions as api_exc
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
    except domain_exc.NotFoundError:
        raise api_exc.EntityNotFoundException('User', user_id)
    except domain_exc.UniqueFieldError:
        raise api_exc.EntityAlreadyExistException('User')
