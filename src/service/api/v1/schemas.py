from uuid import UUID

from pydantic import BaseModel


class WatchingResponse(BaseModel):
    """Класс для краткого описания просмотренного фрейма в ответе API."""

    user_id: UUID
    movie_id: UUID
    frame: str
