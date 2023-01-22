import dataclasses
import enum
import uuid


class PostRateEvent(enum.Enum):
    like = 'like'
    dislike = 'dislike'
    unlike = 'unlike'
    undislike = 'undislike'


@dataclasses.dataclass(slots=True)
class Post:
    id: uuid.UUID  # noqa: VNE003
    user_id: uuid.UUID
    text: str
    likes: int
    dislikes: int
