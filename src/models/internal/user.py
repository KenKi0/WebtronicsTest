import dataclasses
import uuid


@dataclasses.dataclass(slots=True)
class User:
    id: uuid.UUID  # noqa: VNE003
    username: str
    email: str
    password: str
