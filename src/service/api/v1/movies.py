from http import HTTPStatus
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Header, Request, Body
from auth.auth_bearer import JWTBearer
from .schemas import ScoreResponse

router = APIRouter()


@router.post(
    "/add-score",
    response_model=ScoreResponse,
    summary="Добавление оценки к фильму",
    description="Добавление/изменение/удаление оценки к фильму",
    response_description="Оценка фильма",
    tags=["movies"],
    dependencies=[Depends(JWTBearer())],
)
async def add_score(
    request: Request,
    movie_id: UUID = Body(default=None),
    score: int = Body(default=None),
):
    user = request.state.user_id
    return ScoreResponse()


@router.get(
    "/scores",
    response_model=ScoreResponse,
    summary="Получение оценки фильма",
    description="Получение средней оценки фильма, количество лайков/дизлайков",
    response_description="Оценка фильма",
    tags=["movies"],
    dependencies=[Depends(JWTBearer())],
)
async def get_score(request: Request, movie_id: UUID = Body(default=None)):
    user = request.state.user_id
    return ScoreResponse()
