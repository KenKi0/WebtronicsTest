import fastapi

import src.infrastructure.database.repositories as repo
from src.services.auth import IAuthService
from src.services.post import IPostService
from src.services.user import IUserService
from src.utils.auth import Auth, get_auth


def auth_service_provider(
    user_repo: repo.IUserRepository = fastapi.Depends(repo.user_repo_provider),
    auth: Auth = fastapi.Depends(get_auth),
) -> IAuthService:
    ...


def post_service_provider(
    post_repo: repo.IPostRepository = fastapi.Depends(repo.post_repo_provider),
) -> IPostService:
    ...


def user_service_provider(
    user_repo: repo.IUserRepository = fastapi.Depends(repo.user_repo_provider),
    post_repo: repo.IPostRepository = fastapi.Depends(repo.post_repo_provider),
) -> IUserService:
    ...
