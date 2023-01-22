from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.database.models.base import BaseModel


class Posts(BaseModel):
    __tablename__ = 'posts'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    text = Column(Text, nullable=False)
    likes = Column(Integer, nullable=False, default=0)
    dislikes = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f'Post: user - {self.user_id} id - {self.id}'
