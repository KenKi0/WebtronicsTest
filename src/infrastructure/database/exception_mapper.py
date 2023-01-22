from functools import wraps
from typing import Any, Callable

from sqlalchemy.exc import IntegrityError

from src.core.exceptions.repository import UniqueFieldError


def exception_mapper(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def wrapped(*args: Any, **kwargs: Any):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as err:
            raise UniqueFieldError from err

    return wrapped
