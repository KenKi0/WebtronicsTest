import logging
import typing
import uuid
from functools import lru_cache

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession

import src.core.exceptions as exc
import src.infrastructure.database.repositories as repo
import src.models.dto.post as post_internal_mdl
import src.models.http.post as post_http_mdl

logger = logging.getLogger(__name__)


class IPostService(typing.Protocol):
    async def create_post(self, new_post: post_http_mdl.PostCreateRequest, session: AsyncSession) -> None:
        ...

    async def get_post(self, post_id: uuid.UUID, session: AsyncSession) -> post_internal_mdl.Post:
        """
        :raises NotFoundError: if raw with specified post_id doesnt exist
        """
        ...

    async def update_post(
        self,
        post_id: uuid.UUID,
        updated_fields: post_http_mdl.PostUpdateRequest,
        session: AsyncSession,
    ) -> None:
        """
        :raises NotFoundError: if raw with specified post_id doesnt exist
        """
        ...

    async def delete_post(self, post_id: uuid.UUID, session: AsyncSession) -> None:
        """
        :raises NotFoundError: if raw with specified post_id doesnt exist
        """
        ...

    async def rate_post(
        self,
        user_id: str,
        post_id: uuid.UUID,
        rate_event: post_internal_mdl.PostRateEvent,
        session: AsyncSession,
    ) -> None:
        """
        :raises NotFoundError: if raw with specified post_id doesnt exist
        :raises RateYourselfPostsError: if user try to rate yourself posts
        """
        ...


class PostService(IPostService):
    def __init__(
        self,
        post_repo: repo.IPostRepository,
    ):
        self.__post_repo = post_repo

    async def create_post(self, new_post: post_http_mdl.PostCreateRequest, session: AsyncSession) -> None:
        await self.__post_repo.create(new_post, session)

    async def update_post(
        self,
        post_id: uuid.UUID,
        updated_fields: post_http_mdl.PostUpdateRequest,
        session: AsyncSession,
    ) -> None:
        try:
            await self.__post_repo.update(post_id, updated_fields, session)
        except exc.NotFoundError as e:
            logger.info('Trying to update non-existent post with id: %s', post_id, exc_info=e)
            raise

    async def get_post(self, post_id: uuid.UUID, session: AsyncSession) -> post_internal_mdl.Post:
        try:
            return await self.__post_repo.get(post_id, session)
        except exc.NotFoundError as e:
            logger.info('Trying to get non-existent post with id: %s', post_id, exc_info=e)
            raise

    async def delete_post(self, post_id: uuid.UUID, session: AsyncSession) -> None:
        try:
            await self.__post_repo.delete(post_id, session)
        except exc.NotFoundError as e:
            logger.info('Trying to delete non-existent post with id: %s', post_id, exc_info=e)
            raise

    async def rate_post(
        self,
        user_id: str,
        post_id: uuid.UUID,
        rate_event: post_internal_mdl.PostRateEvent,
        session: AsyncSession,
    ) -> None:
        try:
            await self.__post_repo.update_post_rates(user_id, post_id, rate_event, session)
        except exc.NotFoundError as e:
            logger.info('Trying to rate non-existent post with id: %s', post_id, exc_info=e)
            raise
        except exc.RateYourselfPostsError as e:
            logger.info('Trying to rate yourself posts by user_id: %s', user_id, exc_info=e)
            raise


@lru_cache()
def post_service(
    post_repo: repo.IPostRepository = fastapi.Depends(repo.post_repo_provider),
) -> IPostService:
    return PostService(post_repo)


__all__ = [
    'IPostService',
    'post_service',
]
