import typing as t

import fastapi
from fastapi import Request
from fastapi.responses import ORJSONResponse

from src.api.exceptions.exceptions import ICustomException


def custom_exception_handler(request: Request, exc: ICustomException) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=exc.status_code,
        content={'message': exc.message},
    )


def map_exceptions_with_handler(
    app: fastapi.FastAPI,
    exceptions: t.Iterable[t.Type[ICustomException]],
    handler: t.Callable[..., t.Any],
) -> None:
    for exc in exceptions:
        app.add_exception_handler(exc, handler)
