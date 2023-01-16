import fastapi

import src.models.http.auth as auth_http_models
import src.core.exceptions as exc
from src.services import get_auth_service, AuthServiceProtocol

router = fastapi.APIRouter(prefix='/auth')


@router.post('/signup',
             status_code=fastapi.status.HTTP_201_CREATED,
             description='Create new user',
             tags=['Auth'])
async def signup(
        payload: auth_http_models.SignUpRequest,
        service: AuthServiceProtocol = fastapi.Depends(get_auth_service),
):
    try:
        await service.register(payload)
    except exc.NotFoundError:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND,
                                    detail='User not found')


@router.post('/login',
             status_code=fastapi.status.HTTP_200_OK,
             description='Login into service',
             tags=['Auth'])
async def login(
        payload: auth_http_models.LoginRequest,
        service: AuthServiceProtocol = fastapi.Depends(get_auth_service),
):
    try:
        return await service.login(payload)
    except exc.NotFoundError:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND,
                                    detail='User not found')
    except exc.InvalidPassword:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                                    detail='Wrong password')
