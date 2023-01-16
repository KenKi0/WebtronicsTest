from pydantic.networks import EmailStr

from src.models.base import Base


class UserUpdateRequest(Base):
    username: str | None
    email: EmailStr | None
