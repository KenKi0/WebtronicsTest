import typing
import uuid
from functools import lru_cache

import sqlalchemy

import src.models.http.post as post_http_mdl
import src.models.internal.post as post_internal_mdl
import src.core.exceptions as exc
from src.db.sqlalch.models.posts import Posts
from src.db.sqlalch.core import session_maker


class PostRepositoryProtocol(typing.Protocol):

    async def create(self, new_post: post_http_mdl.PostCreateRequest) -> None:
        ...

    async def update(self, post_id: uuid.UUID, updated_fields: post_http_mdl.PostUpdateRequest) -> None:
        """
        :raises NotFoundError: if raw with specified post_id didnt exist
        """
        ...

    async def get(self, post_id: uuid.UUID) -> post_internal_mdl.Post:
        """
        :raises NotFoundError: if raw with specified post_id didnt exist
        """
        ...

    async def delete(self, post_id: uuid.UUID) -> None:
        """
        :raises NotFoundError: if raw with specified post_id didnt exist
        """
        ...

    async def update_post_rates(
            self,
            user_id: str,
            post_id: uuid.UUID,
            updated_event: post_internal_mdl.PostRateEvent
    ) -> None:
        """
        :raises RateYourselfPostsError: if user trying to rate their posts
        :raises NotFoundError: if raw with specified post_id didnt exist
        """
        ...

    async def get_user_posts(self, user_id: uuid.UUID) -> list[post_internal_mdl.Post]:
        ...


class PostSqlalchemyRepository(PostRepositoryProtocol):

    async def create(self, new_post: post_http_mdl.PostCreateRequest) -> None:
        post = Posts(**new_post.dict())
        async with session_maker() as session:
            session.add(post)
            await session.commit()

    async def update(self, post_id: uuid.UUID, updated_fields: post_http_mdl.PostUpdateRequest) -> None:
        query = (sqlalchemy.update(Posts)
                 .where(Posts.id == post_id)
                 .values(**updated_fields.dict(exclude_none=True)))
        async with session_maker() as session:
            result: sqlalchemy.engine.cursor.CursorResult = await session.execute(query)
            if result.rowcount == 0:
                raise exc.NotFoundError
            await session.commit()

    async def get(self, post_id: uuid.UUID) -> post_internal_mdl.Post:
        query = sqlalchemy.select(Posts).where(Posts.id == post_id)
        async with session_maker() as session:
            result: sqlalchemy.engine.Result = await session.execute(query)
            post: Posts | None = result.scalars().one_or_none()
            if post is None:
                raise exc.NotFoundError
        return post_internal_mdl.Post(**post.as_dict(exclude_non_tabel_columns=True))

    async def delete(self, post_id: uuid.UUID) -> None:
        query = sqlalchemy.delete(Posts).where(Posts.id == post_id)
        async with session_maker() as session:
            result: sqlalchemy.engine.cursor.CursorResult = await session.execute(query)
            if result.rowcount == 0:
                raise exc.NotFoundError
            await session.commit()

    async def update_post_rates(
            self,
            user_id: str,
            post_id: uuid.UUID,
            updated_event: post_internal_mdl.PostRateEvent
    ) -> None:
        query = sqlalchemy.select(Posts).where(Posts.id == post_id)
        async with session_maker() as session:
            result: sqlalchemy.engine.Result = await session.execute(query)
            post: Posts | None = result.scalars().one_or_none()
            if str(post.user_id) == user_id:
                raise exc.RateYourselfPostsError
            if post is None:
                raise exc.NotFoundError
            match updated_event:
                case post_internal_mdl.PostRateEvent.like:
                    post.likes += 1
                case post_internal_mdl.PostRateEvent.dislike:
                    post.dislikes += 1
                case post_internal_mdl.PostRateEvent.unlike:
                    post.likes -= 1
                case post_internal_mdl.PostRateEvent.undislike:
                    post.dislikes -= 1
            await session.commit()

    async def get_user_posts(self, user_id: uuid.UUID) -> list[post_internal_mdl.Post]:
        query = sqlalchemy.select(Posts).where(Posts.user_id == user_id)
        async with session_maker() as session:
            result: sqlalchemy.engine.Result = await session.execute(query)
            posts: list[Posts] = result.scalars().all()
        return [post_internal_mdl.Post(**post.as_dict(exclude_non_tabel_columns=True)) for post in posts]


@lru_cache()
def get_post_repo() -> PostRepositoryProtocol:
    return PostSqlalchemyRepository()


__all__ = [
    'PostRepositoryProtocol',
    'get_post_repo',
]
