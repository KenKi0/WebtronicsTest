import logging
import typing
import uuid
from functools import lru_cache

import fastapi

import src.models.http.post as post_http_mdl
import src.models.internal.post as post_internal_mdl
import src.repositories as repo
import src.core.exceptions as exc


logger = logging.getLogger(__name__)


class PostServiceProtocol(typing.Protocol):

    async def create_post(self, new_post: post_http_mdl.PostCreateRequest) -> None:
        ...

    async def get_post(self, post_id: uuid.UUID) -> post_internal_mdl.Post:
        """
        :raises NotFoundError: if raw with specified post_id doesnt exist
        """
        ...

    async def update_post(self, post_id: uuid.UUID, updated_fields: post_http_mdl.PostUpdateRequest) -> None:
        """
        :raises NotFoundError: if raw with specified post_id doesnt exist
        """
        ...

    async def delete_post(self, post_id: uuid.UUID) -> None:
        """
        :raises NotFoundError: if raw with specified post_id doesnt exist
        """
        ...

    async def rate_post(
            self,
            user_id: str,
            post_id: uuid.UUID,
            rate_event: post_internal_mdl.PostRateEvent,
    ) -> None:
        """
        :raises NotFoundError: if raw with specified post_id doesnt exist
        :raises RateYourselfPostsError: if user try to rate yourself posts
        """
        ...


class PostService(PostServiceProtocol):

    def __init__(
            self,
            post_repo: repo.PostRepositoryProtocol,
    ):
        self.__post_repo = post_repo

    async def create_post(self, new_post: post_http_mdl.PostCreateRequest) -> None:
        await self.__post_repo.create(new_post)

    async def update_post(self, post_id: uuid.UUID, updated_fields: post_http_mdl.PostUpdateRequest) -> None:
        try:
            await self.__post_repo.update(post_id, updated_fields)
        except exc.NotFoundError as e:
            logger.info('Trying to update non-existent post with id: %s', post_id, exc_info=e)
            raise

    async def get_post(self, post_id: uuid.UUID) -> post_internal_mdl.Post:
        try:
            return await self.__post_repo.get(post_id)
        except exc.NotFoundError as e:
            logger.info('Trying to get non-existent post with id: %s', post_id, exc_info=e)
            raise

    async def delete_post(self, post_id: uuid.UUID) -> None:
        try:
            await self.__post_repo.delete(post_id)
        except exc.NotFoundError as e:
            logger.info('Trying to delete non-existent post with id: %s', post_id, exc_info=e)
            raise

    async def rate_post(
            self,
            user_id: str,
            post_id: uuid.UUID,
            rate_event: post_internal_mdl.PostRateEvent,
    ) -> None:
        try:
            await self.__post_repo.update_post_rates(user_id, post_id, rate_event)
        except exc.NotFoundError as e:
            logger.info('Trying to rate non-existent post with id: %s', post_id, exc_info=e)
            raise
        except exc.RateYourselfPostsError as e:
            logger.info('Trying to rate yourself posts by user_id: %s', user_id, exc_info=e)
            raise


@lru_cache()
def get_post_service(
        post_repo: repo.PostRepositoryProtocol = fastapi.Depends(repo.get_post_repo),
) -> PostServiceProtocol:
    return PostService(post_repo)


__all__ = [
    'PostServiceProtocol',
    'get_post_service',
]
