from src.infrastructure.database.repositories.post import IPostRepository, post_repo
from src.infrastructure.database.repositories.providers import post_repo_provider, user_repo_provider
from src.infrastructure.database.repositories.user import IUserRepository, user_repo

__all__ = [
    'IUserRepository',
    'IPostRepository',
    'post_repo',
    'user_repo',
    'post_repo_provider',
    'user_repo_provider',
]
