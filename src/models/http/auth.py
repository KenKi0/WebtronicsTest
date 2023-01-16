from pydantic import root_validator
from pydantic.networks import EmailStr

from src.models.base import Base


class SignUpRequest(Base):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

    @root_validator()
    def verify_password_match(cls, values):
        password = values.get("password")
        confirm_password = values.get("confirm_password")

        if password != confirm_password:
            raise ValueError("The two passwords did not match.")
        return values


class LoginRequest(Base):
    email: EmailStr
    password: str
