from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class WatchingResponse(BaseModel):
    """Класс для краткого описания просмотренного фрейма в ответе API."""

    user_id: UUID
    movie_id: UUID
    frame: str


class UUIDMixin(BaseModel):
    user_id: UUID | None = None
    movie_id: UUID | None = None


class ReviewResponse(UUIDMixin, BaseModel):
    review_id: UUID
    text: str | None = None
    pub_dt: datetime | None = None
    score: int


class ScoreReviewResponse(UUIDMixin, BaseModel):
    review_id: UUID
    score: int


class ScoreResponse(UUIDMixin, BaseModel):
    score: int
    avg_score: float | None = None
    like_cnt: int | None = None
    dislike_cnt: int | None = None


class BookmarkResponse(BaseModel):
    user_id: UUID
    movie_id: UUID
