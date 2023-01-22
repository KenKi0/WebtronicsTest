import logging
import typing
import uuid
from functools import lru_cache

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

import src.core.exceptions as exc
import src.infrastructure.database.repositories as repo
import src.models.dto.post as post_internal_mdl
import src.models.http.user as user_http_mdl

logger = logging.getLogger(__name__)


class IUserService(typing.Protocol):
    async def update_user_info(
        self,
        user_id: uuid.UUID,
        updated_fields: user_http_mdl.UserUpdateRequest,
        session: AsyncSession,
    ) -> None:
        """
        :raises NotFoundError: if raw with specified user_id doesnt exist
        :raises UniqueFieldError: if a constraint error occurs during update user fields
        """
        ...

    async def get_user_posts(self, user_id: uuid.UUID, session: AsyncSession) -> list[post_internal_mdl.Post]:
        ...


class UserService(IUserService):
    def __init__(
        self,
        user_repo: repo.IUserRepository,
        post_repo: repo.IPostRepository,
    ):
        self.__post_repo = post_repo
        self.__user_repo = user_repo

    async def update_user_info(
        self,
        user_id: uuid.UUID,
        updated_fields: user_http_mdl.UserUpdateRequest,
        session: AsyncSession,
    ) -> None:
        try:
            await self.__user_repo.update(user_id, updated_fields, session)
        except exc.NotFoundError as e:
            logger.info('Trying to update non-existent user with id: %s', user_id, exc_info=e)
            raise
        except exc.UniqueFieldError as e:
            logger.info('Constraint error during update user fields', exc_info=e)
            raise

    async def get_user_posts(self, user_id: uuid.UUID, session: AsyncSession) -> list[post_internal_mdl.Post]:
        return await self.__post_repo.get_user_posts(user_id, session)


@lru_cache()
def user_service(
    user_repo: repo.IUserRepository = fastapi.Depends(repo.user_repo_provider),
    post_repo: repo.IPostRepository = fastapi.Depends(repo.post_repo_provider),
) -> IUserService:
    return UserService(user_repo, post_repo)


__all__ = [
    'IUserService',
    'user_service',
]
