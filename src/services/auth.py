import logging
import typing
from functools import lru_cache

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

import src.core.exceptions as domain_exc
import src.infrastructure.database.repositories as repo
import src.models.http.auth as auth_http_models
from src.utils.auth import Auth, get_auth

logger = logging.getLogger(__name__)


class IAuthService(typing.Protocol):
    async def register(self, new_user: auth_http_models.SignUpRequest, session: AsyncSession) -> None:
        """
        :raises UniqueFieldError: if raw with specified new user fields already exist
        """
        ...

    async def login(self, user_credentials: auth_http_models.LoginRequest, session: AsyncSession) -> tuple[str, str]:
        """
        :raises NotFoundError: if raw with specified user credentials doesnt exist
        :raises InvalidPassword: if specified password doesnt match with password in db
        """
        ...

    async def refresh_token(self, refresh_token: str) -> tuple[str, str]:
        ...


class AuthService(IAuthService):
    def __init__(
        self,
        user_repo: repo.IUserRepository,
        auth: Auth,
    ):
        self.__user_repo = user_repo
        self.__auth = auth

    async def register(self, new_user: auth_http_models.SignUpRequest, session: AsyncSession) -> None:
        new_user.password = self.__auth.get_password_hash(new_user.password)
        try:
            await self.__user_repo.create(new_user, session)
        except domain_exc.UniqueFieldError as e:
            logger.info('Trying to register user with existing field', exc_info=e)
            raise

    async def login(self, user_credentials: auth_http_models.LoginRequest, session: AsyncSession) -> tuple[str, str]:
        try:
            user = await self.__user_repo.get_by_email(user_credentials.email, session)
        except domain_exc.NotFoundError as e:
            logger.info('Trying to login to non-existent account', exc_info=e)
            raise
        if not self.__auth.verify_password(user_credentials.password, user.password):
            raise domain_exc.InvalidPassword
        access_token = self.__auth.encode_token(user.id)
        refresh_token = self.__auth.encode_refresh_token(user.id)
        return access_token, refresh_token

    async def refresh_token(self, refresh_token: str) -> tuple[str, str]:
        new_access_token, new_refresh_token = self.__auth.refresh_tokens(refresh_token)
        return new_access_token, new_refresh_token


@lru_cache()
def auth_service(
    user_repo: repo.IUserRepository = fastapi.Depends(repo.user_repo_provider),
    auth: Auth = fastapi.Depends(get_auth),
) -> IAuthService:
    return AuthService(user_repo, auth)


__all__ = [
    'IAuthService',
    'auth_service',
]
