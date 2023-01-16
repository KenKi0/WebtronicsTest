import fastapi

import src.api.v1.healthcheck as healthcheck_routing
import src.api.v1.auth as auth_routing
import src.api.v1.user as user_routing
import src.api.v1.post as post_routing

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


__all__ = [
    'v1_app',
]
