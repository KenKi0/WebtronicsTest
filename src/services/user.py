import logging
import typing
import uuid
from functools import lru_cache

import fastapi

import src.models.http.user as user_http_mdl
import src.models.internal.post as post_internal_mdl
import src.repositories as repo
import src.core.exceptions as exc


logger = logging.getLogger(__name__)


class UserServiceProtocol(typing.Protocol):

    async def update_user_info(self, user_id: uuid.UUID, updated_fields: user_http_mdl.UserUpdateRequest) -> None:
        """
        :raises NotFoundError: if raw with specified user_id doesnt exist
        :raises UniqueFieldError: if a constraint error occurs during update user fields
        """
        ...

    async def get_user_posts(self, user_id: uuid.UUID) -> list[post_internal_mdl.Post]:
        ...


class UserService(UserServiceProtocol):

    def __init__(
            self,
            user_repo: repo.UserRepositoryProtocol,
            post_repo: repo.PostRepositoryProtocol,
    ):
        self.__post_repo = post_repo
        self.__user_repo = user_repo

    async def update_user_info(self, user_id: uuid.UUID, updated_fields: user_http_mdl.UserUpdateRequest) -> None:
        try:
            await self.__user_repo.update(user_id, updated_fields)
        except exc.NotFoundError as e:
            logger.info('Trying to update non-existent user with id: %s', user_id, exc_info=e)
            raise
        except exc.UniqueFieldError as e:
            logger.info('Constraint error during update user fields', exc_info=e)
            raise

    async def get_user_posts(self, user_id: uuid.UUID) -> list[post_internal_mdl.Post]:
        return await self.__post_repo.get_user_posts(user_id)


@lru_cache()
def get_user_service(
        user_repo: repo.UserRepositoryProtocol = fastapi.Depends(repo.get_user_repo),
        post_repo: repo.PostRepositoryProtocol = fastapi.Depends(repo.get_post_repo),
) -> UserServiceProtocol:
    return UserService(user_repo, post_repo)


__all__ = [
    'UserServiceProtocol',
    'get_user_service',
]
