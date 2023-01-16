from src.repositories.user import UserRepositoryProtocol, get_user_repo
from src.repositories.post import PostRepositoryProtocol, get_post_repo


__all__ = [
    'UserRepositoryProtocol',
    'PostRepositoryProtocol',
    'get_post_repo',
    'get_user_repo',
]
