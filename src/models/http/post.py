import uuid

from src.models.base import Base


class PostCreateRequest(Base):
    user_id: uuid.UUID
    text: str


class PostUpdateRequest(Base):
    text: str


class PostResponse(Base):
    id: uuid.UUID  # noqa: VNE003
    user_id: uuid.UUID
    text: str
    likes: int
    dislikes: int
