from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Header, Request, Body
from auth.auth_bearer import JWTBearer
from .schemas import ScoreRequest, ScoreResponse

router = APIRouter()

@router.post(
    "/add-score",
    response_model=ScoreResponse,
    summary="Добавление оценки к фильму",
    description="Добавление/изменение/удаление оценки к фильму",
    response_description="Рецензия",
    tags=["movies"],
    dependencies=[Depends(JWTBearer())]
)
async def add_score(request: Request, review: ScoreRequest = Body(default=None)):
    return ScoreResponse()



@router.get(
    "/scores",
    response_model=ScoreResponse,
    summary="Получение оценки фильма",
    description="Получение средней оценки фильма, количество лайков/дизлайков",
    response_description="Оценка фильма",
    tags=["movies"],
    dependencies=[Depends(JWTBearer())]
)
async def get_score(request: Request, review: ScoreRequest = Body(default=None)):
    return ScoreResponse()