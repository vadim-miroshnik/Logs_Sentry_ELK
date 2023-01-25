from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class WatchingResponse(BaseModel):
    """Класс для краткого описания просмотренного фрейма в ответе API."""

    user_id: UUID
    movie_id: UUID
    frame: str


class ReviewRequest(BaseModel):
    review_id: UUID
    text: str | None = None
    pub_dt: datetime | None = None
    score: int


class ReviewResponse(BaseModel):
    review_id: UUID
    text: str | None = None
    pub_dt: datetime | None = None
    score: int


class ScoreReviewRequest(BaseModel):
    review_id: UUID
    score: int


class ScoreReviewResponse(BaseModel):
    review_id: UUID
    score: int


class ScoreRequest(BaseModel):
    movie_id: UUID
    score: int


class ScoreResponse(BaseModel):
    movie_id: UUID
    score: int
    avg_score: float
    like_cnt: int
    dislike_cnt: int
