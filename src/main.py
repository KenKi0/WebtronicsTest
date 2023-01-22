import fastapi

import src.api.v1 as v1_api
import src.infrastructure.database.repositories as repo
import src.services as services
from src.core.config import settings
from src.infrastructure.database.core import get_session, session_provider

app = fastapi.FastAPI(
    title=settings.project_name,
    description='Webtronics Test Service',
    version='1',
    default_response_class=fastapi.responses.ORJSONResponse,
)

app.mount('/api/v1', v1_api.v1_app)

app.dependency_overrides[services.user_service_provider] = services.user_service
app.dependency_overrides[services.auth_service_provider] = services.auth_service
app.dependency_overrides[services.post_service_provider] = services.post_service
app.dependency_overrides[repo.post_repo_provider] = repo.post_repo
app.dependency_overrides[repo.user_repo_provider] = repo.user_repo
app.dependency_overrides[session_provider] = get_session
