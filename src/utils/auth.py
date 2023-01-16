import uuid
from functools import lru_cache
from datetime import datetime, timedelta

import jwt
import fastapi
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

from src.core.config import settings


class Auth:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id: uuid.UUID) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=settings.jwt_settings.access_token_expire),
            'iat': datetime.utcnow(),
            'sub': str(user_id)
        }
        return jwt.encode(
            payload,
            settings.jwt_settings.secret_key,
            algorithm=settings.jwt_settings.algorithm,
        )

    @staticmethod
    def decode_token(token: str) -> uuid.UUID:
        try:
            payload = jwt.decode(token,
                                 settings.jwt_settings.secret_key,
                                 algorithms=[settings.jwt_settings.algorithm])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                                        detail='Signature has expired')
        except jwt.InvalidTokenError:
            raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                                        detail='Invalid token')

    @staticmethod
    def encode_refresh_token(user_id: uuid.UUID) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=settings.jwt_settings.refresh_token_expire),
            'iat': datetime.utcnow(),
            'scope': 'refresh_token',
            'sub': str(user_id)
        }
        return jwt.encode(
            payload,
            settings.jwt_settings.secret_key,
            algorithm=settings.jwt_settings.algorithm,
        )

    def refresh_tokens(self, refresh_token) -> tuple[str, str]:
        try:
            payload = jwt.decode(refresh_token,
                                 settings.jwt_settings.secret_key,
                                 algorithms=[settings.jwt_settings.algorithm])
            if payload['scope'] == 'refresh_token':
                user_id = payload['sub']
                new_token = self.encode_token(user_id)
                new_refresh_token = self.encode_refresh_token(user_id)
                return new_token, new_refresh_token
            raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                                        detail='Invalid scope for token')
        except jwt.ExpiredSignatureError:
            raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                                        detail='Refresh token expired')
        except jwt.InvalidTokenError:
            raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                                        detail='Invalid refresh token')

    @staticmethod
    def login_required(credentials: HTTPAuthorizationCredentials = fastapi.Security(security)) -> uuid.UUID:
        token = credentials.credentials
        return Auth.decode_token(token)


@lru_cache()
def get_auth() -> Auth:
    return Auth()
