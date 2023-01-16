import orjson
import pydantic


def orjson_dumps(value, *, default):
    return orjson.dumps(value, default=default).decode()


class Base(pydantic.BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
