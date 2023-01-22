from sqlalchemy.ext.asyncio import AsyncSession


async def session_provider() -> AsyncSession:
    ...
