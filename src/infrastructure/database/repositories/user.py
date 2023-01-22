import typing
import uuid
from functools import lru_cache

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

import src.core.exceptions as exc
import src.models.dto.user as user_internal_models
import src.models.http.auth as auth_http_mdl
import src.models.http.user as user_http_mdl
from src.infrastructure.database.exception_mapper import exception_mapper
from src.infrastructure.database.models.user import User


class IUserRepository(typing.Protocol):
    async def get_by_email(self, email: str, session: AsyncSession) -> user_internal_models.User:
        ...

    async def create(self, new_user: auth_http_mdl.SignUpRequest, session: AsyncSession) -> None:
        """
        :raises UniqueFieldError: if raw with specified updated fields already exist, only for unique fields
        """
        ...

    async def update(
        self,
        user_id: uuid.UUID,
        updated_fields: user_http_mdl.UserUpdateRequest,
        session: AsyncSession,
    ) -> None:
        """
        :raises NotFoundError: if raw with specified user_id didnt exist
        :raises UniqueFieldError: if raw with specified updated fields already exist, only for unique fields
        """
        ...


class UserSqlalchemyRepositoryProtocol(IUserRepository):
    async def get_by_email(self, email: str, session: AsyncSession) -> user_internal_models.User:
        query = sqlalchemy.select(User).where(User.email == email)
        result: sqlalchemy.engine.cursor.CursorResult = await session.execute(query)  # type: ignore
        user: User | None = result.scalars().one_or_none()
        if user is None:
            raise exc.NotFoundError
        await session.commit()
        return user_internal_models.User(**user.as_dict(exclude_non_tabel_columns=True))

    @exception_mapper
    async def create(self, new_user: auth_http_mdl.SignUpRequest, session: AsyncSession) -> None:
        user = User(**new_user.dict(exclude={'confirm_password'}))
        session.add(user)
        await session.commit()

    @exception_mapper
    async def update(
        self,
        user_id: uuid.UUID,
        updated_fields: user_http_mdl.UserUpdateRequest,
        session: AsyncSession,
    ) -> None:
        query = sqlalchemy.update(User).where(User.id == user_id).values(**updated_fields.dict(exclude_none=True))
        result: sqlalchemy.engine.cursor.CursorResult = await session.execute(query)  # type: ignore
        if result.rowcount == 0:
            raise exc.NotFoundError
        await session.commit()


@lru_cache()
def user_repo() -> IUserRepository:
    return UserSqlalchemyRepositoryProtocol()


__all__ = [
    'IUserRepository',
    'user_repo',
]
