from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Header, Request, Body
from auth.auth_bearer import JWTBearer
from .schemas import BookmarkResponse

router = APIRouter()


@router.post(
    "/add-bookmark",
    response_model=BookmarkResponse,
    summary="Добавление закладки на фильм",
    description="Добавление/изменение/удаление закладки на фильм",
    response_description="Закладка на фильм",
    tags=["bookmarks"],
    dependencies=[Depends(JWTBearer())]
)
async def add_score(request: Request, movie_id: UUID = Body(default=None)):
    user = request.state.user_id
    return BookmarkResponse()


@router.get(
    "/bookmarks",
    response_model=list[BookmarkResponse],
    summary="Получение закладок на фильмы",
    description="Получение закладок на фильмы",
    response_description="Список закладок на фильмы",
    tags=["bookmarks"],
    dependencies=[Depends(JWTBearer())]
)
async def get_score(request: Request):
    user = request.state.user_id
    return BookmarkResponse()
