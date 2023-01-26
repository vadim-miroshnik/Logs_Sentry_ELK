from http import HTTPStatus
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Header, Request, Body
from auth.auth_bearer import JWTBearer
from .schemas import ReviewResponse

router = APIRouter()


@router.post(
    "/add-review",
    response_model=ReviewResponse,
    summary="Создание рецензии на фильм",
    description="При создании рецензии передается текст, дата публикации и оценка фильма. При обновлении рецензии передается её идентификатор",
    response_description="Рецензия",
    tags=["reviews"],
    dependencies=[Depends(JWTBearer())],
)
async def add_review(
    request: Request,
    review_id: UUID = Body(default=None),
    text: str = Body(default=None),
    pub_dt: datetime = Body(default=None),
    score: int = Body(default=None),
):
    user = request.state.user_id
    return ReviewResponse()


@router.post(
    "/score-review",
    response_model=ReviewResponse,
    summary="Оценка рецензии на фильм",
    description="Оценка рецензии на фильм",
    response_description="Оценка",
    tags=["reviews"],
    dependencies=[Depends(JWTBearer())],
)
async def score_review(
    request: Request,
    review_id: UUID = Body(default=None),
    score: int = Body(default=None),
):
    user = request.state.user_id
    return ReviewResponse()


@router.get(
    "/reviews",
    response_model=list[ReviewResponse],
    summary="Получение списка рецензий",
    description="Получение списка рецензий с возможностью гибкой сортировки",
    response_description="Список рецензий",
    tags=["reviews"],
    dependencies=[Depends(JWTBearer())],
)
async def get_reviews(request: Request, movie_id: UUID = Body(default=None)):
    user = request.state.user_id
    return ""
