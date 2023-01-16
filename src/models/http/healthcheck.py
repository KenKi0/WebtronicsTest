from src.models.base import Base


class Healthcheck(Base):
    project_name: str
    version: str
    health: bool
