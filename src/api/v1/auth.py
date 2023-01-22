import fastapi

import src.core.exceptions as exc
import src.models.http.auth as auth_http_models
from src.infrastructure.database.core import AsyncSession, session_provider
from src.services import IAuthService, auth_service_provider

router = fastapi.APIRouter(prefix='/auth')


@router.post('/signup', status_code=fastapi.status.HTTP_201_CREATED, description='Create new user', tags=['Auth'])
async def signup(
    payload: auth_http_models.SignUpRequest,
    service: IAuthService = fastapi.Depends(auth_service_provider),
    session: AsyncSession = fastapi.Depends(session_provider),
):
    try:
        await service.register(payload, session)
    except exc.NotFoundError:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail='User not found')


@router.post('/login', status_code=fastapi.status.HTTP_200_OK, description='Login into service', tags=['Auth'])
async def login(
    payload: auth_http_models.LoginRequest,
    service: IAuthService = fastapi.Depends(auth_service_provider),
    session: AsyncSession = fastapi.Depends(session_provider),
):
    try:
        return await service.login(payload, session)
    except exc.NotFoundError:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail='User not found')
    except exc.InvalidPassword:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail='Wrong password')
