from src.infrastructure.database.repositories.post import IPostRepository
from src.infrastructure.database.repositories.user import IUserRepository


def post_repo_provider() -> IPostRepository:
    ...


def user_repo_provider() -> IUserRepository:
    ...
