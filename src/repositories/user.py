import typing
import uuid
from functools import lru_cache

import sqlalchemy
import sqlalchemy.exc as sqlalch_exc

import src.models.http.user as user_http_mdl
import src.models.http.auth as auth_http_mdl
import src.models.internal.user as user_internal_models
import src.core.exceptions as exc
from src.db.sqlalch.models.user import User
from src.db.sqlalch.core import session_maker


class UserRepositoryProtocol(typing.Protocol):

    async def get_by_email(self, email: str) -> user_internal_models.User:
        ...

    async def create(self, new_user: auth_http_mdl.SignUpRequest) -> None:
        """
        :raises UniqueFieldError: if raw with specified updated fields already exist, only for unique fields
        """
        ...

    async def update(self, user_id: uuid.UUID, updated_fields: user_http_mdl.UserUpdateRequest) -> None:
        """
        :raises NotFoundError: if raw with specified user_id didnt exist
        :raises UniqueFieldError: if raw with specified updated fields already exist, only for unique fields
        """
        ...


class UserSqlalchemyRepositoryProtocol(UserRepositoryProtocol):

    async def get_by_email(self, email: str) -> user_internal_models.User:
        query = sqlalchemy.select(User).where(User.email == email)
        async with session_maker() as session:
            result: sqlalchemy.engine.cursor.CursorResult = await session.execute(query)
            user: User | None = result.scalars().one_or_none()
            if user is None:
                raise exc.NotFoundError
            await session.commit()
        return user_internal_models.User(**user.as_dict(exclude_non_tabel_columns=True))

    async def create(self, new_user: auth_http_mdl.SignUpRequest) -> None:
        user = User(**new_user.dict(exclude={'confirm_password'}))
        try:
            async with session_maker() as session:
                session.add(user)
                await session.commit()
        except sqlalch_exc.IntegrityError as e:
            raise exc.UniqueFieldError from e

    async def update(self, user_id: uuid.UUID, updated_fields: user_http_mdl.UserUpdateRequest) -> None:
        query = (sqlalchemy.update(User)
                 .where(User.id == user_id)
                 .values(**updated_fields.dict(exclude_none=True)))
        try:
            async with session_maker() as session:
                result: sqlalchemy.engine.cursor.CursorResult = await session.execute(query)
                if result.rowcount == 0:
                    raise exc.NotFoundError
                await session.commit()
        except sqlalch_exc.IntegrityError as e:
            raise exc.UniqueFieldError from e


@lru_cache()
def get_user_repo() -> UserRepositoryProtocol:
    return UserSqlalchemyRepositoryProtocol()


__all__ = [
    'UserRepositoryProtocol',
    'get_user_repo',
]
