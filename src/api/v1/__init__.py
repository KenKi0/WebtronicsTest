import fastapi

import src.api.v1.auth as auth_routing
import src.api.v1.healthcheck as healthcheck_routing
import src.api.v1.post as post_routing
import src.api.v1.user as user_routing
import src.infrastructure.database.repositories as repo
import src.services as services
from src.api.exceptions import CUSTOM_EXCEPTIONS, custom_exception_handler, map_exceptions_with_handler
from src.infrastructure.database.core import get_session, session_provider

v1_app = fastapi.FastAPI(
    version='1',
    redoc_url='/docs/redoc',
    docs_url='/docs/openapi',
    openapi_url='/docs/openapi.json',
    default_response_class=fastapi.responses.ORJSONResponse,
)

v1_app.include_router(healthcheck_routing.router, tags=['healthcheck'])
v1_app.include_router(auth_routing.router)
v1_app.include_router(user_routing.router)
v1_app.include_router(post_routing.router)


v1_app.dependency_overrides[services.user_service_provider] = services.user_service
v1_app.dependency_overrides[services.auth_service_provider] = services.auth_service
v1_app.dependency_overrides[services.post_service_provider] = services.post_service
v1_app.dependency_overrides[repo.post_repo_provider] = repo.post_repo
v1_app.dependency_overrides[repo.user_repo_provider] = repo.user_repo
v1_app.dependency_overrides[session_provider] = get_session
map_exceptions_with_handler(v1_app, CUSTOM_EXCEPTIONS, custom_exception_handler)


__all__ = [
    'v1_app',
]
