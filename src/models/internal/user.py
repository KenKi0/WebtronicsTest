import dataclasses
import uuid


@dataclasses.dataclass(slots=True)
class User:
    id: uuid.UUID
    username: str
    email: str
    password: str
