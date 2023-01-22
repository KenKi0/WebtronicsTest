import functools
import typing
from pathlib import Path

from pydantic import BaseSettings

LogLevel = typing.Literal['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']


class BaseConfig(BaseSettings):
    class Config:
        __BASE_DIR_PATH = Path(__file__).parent.parent.parent
        __ENV_FILE_PATH = __BASE_DIR_PATH / 'deployment' / '.env'

        env_file = __ENV_FILE_PATH
        env_file_encoding = 'utf-8'


class PostgresSettings(BaseConfig):
    host: str = 'localhost'
    port: int = 5432
    db: str = 'test'
    user: str = 'postgres'
    password: str = 'nipomu54'

    class Config:
        env_prefix = 'PG_'

    @property
    def url(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'


class JWTSettings(BaseConfig):
    secret_key: str = '245585dbb5cbe2f151742298d61d364880575bff0bdcbf4ae383f0180e7e47dd'
    algorithm: str = 'HS256'
    access_token_expire: int = 10  # minutes
    refresh_token_expire: int = 10  # hours

    class Config:
        env_prefix = 'JWT_'


class ProjectSettings(BaseConfig):
    project_name: str = 'Webtronics Test'
    project_host: str = '0.0.0.0'
    project_port: int = 8000
    postgres_settings: PostgresSettings = PostgresSettings()
    jwt_settings: JWTSettings = JWTSettings()

    debug: bool = True
    logs_min_level: LogLevel = 'DEBUG'
    logs_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


@functools.lru_cache()
def _build_settings() -> ProjectSettings:
    return ProjectSettings()


settings = _build_settings()


__all__ = [
    'ProjectSettings',
    'settings',
]
