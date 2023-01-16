from sqlalchemy import Column, String

from src.db.sqlalch.models.base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    username = Column(String(length=150), nullable=False, index=True)
    password = Column(String(length=150), nullable=False)
    email = Column(String(length=150), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'User: {self.username} {self.id}'
