from src.services.auth import AuthServiceProtocol, get_auth_service
from src.services.user import UserServiceProtocol, get_user_service
from src.services.post import PostServiceProtocol, get_post_service


__all__ = [
    'AuthServiceProtocol',
    'get_auth_service',
    'UserServiceProtocol',
    'get_user_service',
    'PostServiceProtocol',
    'get_post_service',
]
