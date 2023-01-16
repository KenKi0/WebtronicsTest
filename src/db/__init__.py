import asyncio

from src.db.sqlalch.core import Base, init_models
from src.db.sqlalch.models.user import User
from src.db.sqlalch.models.posts import Posts


if __name__ == '__main__':
    asyncio.run(init_models())

