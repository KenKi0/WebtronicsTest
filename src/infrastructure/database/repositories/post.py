import typing
import uuid
from functools import lru_cache

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

import src.core.exceptions as exc
import src.models.dto.post as post_internal_mdl
import src.models.http.post as post_http_mdl
from src.infrastructure.database.models.posts import Posts


class IPostRepository(typing.Protocol):
    async def create(self, new_post: post_http_mdl.PostCreateRequest, session: AsyncSession) -> None:
        ...

    async def update(
        self,
        post_id: uuid.UUID,
        updated_fields: post_http_mdl.PostUpdateRequest,
        session: AsyncSession,
    ) -> None:
        """
        :raises NotFoundError: if raw with specified post_id didnt exist
        """
        ...

    async def get(self, post_id: uuid.UUID, session: AsyncSession) -> post_internal_mdl.Post:
        """
        :raises NotFoundError: if raw with specified post_id didnt exist
        """
        ...

    async def delete(self, post_id: uuid.UUID, session: AsyncSession) -> None:
        """
        :raises NotFoundError: if raw with specified post_id didnt exist
        """
        ...

    async def update_post_rates(
        self,
        user_id: str,
        post_id: uuid.UUID,
        updated_event: post_internal_mdl.PostRateEvent,
        session: AsyncSession,
    ) -> None:
        """
        :raises RateYourselfPostsError: if user trying to rate their posts
        :raises NotFoundError: if raw with specified post_id didnt exist
        """
        ...

    async def get_user_posts(self, user_id: uuid.UUID, session: AsyncSession) -> list[post_internal_mdl.Post]:
        ...


class PostSqlalchemyRepository(IPostRepository):
    async def create(self, new_post: post_http_mdl.PostCreateRequest, session: AsyncSession) -> None:
        post = Posts(**new_post.dict())
        session.add(post)
        await session.commit()

    async def update(
        self,
        post_id: uuid.UUID,
        updated_fields: post_http_mdl.PostUpdateRequest,
        session: AsyncSession,
    ) -> None:
        query = sqlalchemy.update(Posts).where(Posts.id == post_id).values(**updated_fields.dict(exclude_none=True))
        result: sqlalchemy.engine.cursor.CursorResult = await session.execute(query)  # type: ignore
        if result.rowcount == 0:
            raise exc.NotFoundError
        await session.commit()

    async def get(self, post_id: uuid.UUID, session: AsyncSession) -> post_internal_mdl.Post:
        query = sqlalchemy.select(Posts).where(Posts.id == post_id)
        result: sqlalchemy.engine.Result = await session.execute(query)
        post: Posts | None = result.scalars().one_or_none()
        if post is None:
            raise exc.NotFoundError
        return post_internal_mdl.Post(**post.as_dict(exclude_non_tabel_columns=True))

    async def delete(self, post_id: uuid.UUID, session: AsyncSession) -> None:
        query = sqlalchemy.delete(Posts).where(Posts.id == post_id)
        result: sqlalchemy.engine.cursor.CursorResult = await session.execute(query)  # type: ignore
        if result.rowcount == 0:
            raise exc.NotFoundError
        await session.commit()

    async def update_post_rates(
        self,
        user_id: str,
        post_id: uuid.UUID,
        updated_event: post_internal_mdl.PostRateEvent,
        session: AsyncSession,
    ) -> None:
        query = sqlalchemy.select(Posts).where(Posts.id == post_id)
        result: sqlalchemy.engine.Result = await session.execute(query)
        post: Posts | None = result.scalars().one_or_none()
        if post is None:
            raise exc.NotFoundError
        if str(post.user_id) == user_id:
            raise exc.RateYourselfPostsError
        match updated_event:
            case post_internal_mdl.PostRateEvent.like:
                post.likes += 1  # type: ignore
            case post_internal_mdl.PostRateEvent.dislike:
                post.dislikes += 1  # type: ignore
            case post_internal_mdl.PostRateEvent.unlike:
                post.likes -= 1  # type: ignore
            case post_internal_mdl.PostRateEvent.undislike:
                post.dislikes -= 1  # type: ignore
        await session.commit()

    async def get_user_posts(self, user_id: uuid.UUID, session: AsyncSession) -> list[post_internal_mdl.Post]:
        query = sqlalchemy.select(Posts).where(Posts.user_id == user_id)
        result: sqlalchemy.engine.Result = await session.execute(query)
        posts: list[Posts] = result.scalars().all()
        return [post_internal_mdl.Post(**post.as_dict(exclude_non_tabel_columns=True)) for post in posts]


@lru_cache()
def post_repo() -> IPostRepository:
    return PostSqlalchemyRepository()


__all__ = [
    'IPostRepository',
    'post_repo',
]
