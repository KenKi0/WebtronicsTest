import fastapi

import src.models.http.healthcheck as http_healthcheck
from src.core.config import settings

router = fastapi.APIRouter(prefix='/healthcheck')


@router.get('/',
            response_model=http_healthcheck.Healthcheck,
            status_code=fastapi.status.HTTP_200_OK,
            description='Check service status')
async def check_healthcheck(
        request: fastapi.Request,
) -> http_healthcheck.Healthcheck:
    return http_healthcheck.Healthcheck(
        project_name=settings.project_name,
        version=request.app.version,
        health=True,
    )
