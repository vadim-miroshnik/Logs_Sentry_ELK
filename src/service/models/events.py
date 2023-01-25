import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ViewEvent(BaseOrjsonModel):

    user_id: str
    movie_id: str
    viewed_frame: int

    def __str__(self):
        return f"{self.user_id} -- {self.movie_id} -- {self.viewed_frame}"
