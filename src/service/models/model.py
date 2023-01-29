from uuid import UUID
import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class MovieScore(BaseOrjsonModel):
    user_id: UUID
    movie_id: UUID
    score: int = Field(ge=0, le=10)


class ReviewScore(BaseOrjsonModel):
    user_id: UUID
    review_id: UUID
    score: int = Field(ge=0, le=10)
