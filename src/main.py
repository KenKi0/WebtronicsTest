import fastapi

import src.api.v1 as v1_api
from src.core.config import settings

app = fastapi.FastAPI(
    title=settings.project_name,
    description='Webtronics Test Service',
    version='1',
    default_response_class=fastapi.responses.ORJSONResponse,
)

app.mount('/api/v1', v1_api.v1_app)
