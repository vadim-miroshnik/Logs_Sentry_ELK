from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Header, Request, Body
from auth.auth_bearer import JWTBearer
from .schemas import ReviewRequest, ReviewResponse, ScoreReviewRequest, ScoreReviewResponse

router = APIRouter()

@router.post(
    "/add-review",
    response_model=ReviewResponse,
    summary="Создание рецензии на фильм",
    description="При создании рецензии передается текст, дата публикации и оценка фильма. При обновлении рецензии передается её идентификатор",
    response_description="Рецензия",
    tags=["reviews"],
    dependencies=[Depends(JWTBearer())]
)
async def add_review(request: Request, review: ReviewRequest = Body(default=None)):
    return ReviewResponse()


@router.post(
    "/score-review",
    response_model=None,
    summary="Оценка рецензии на фильм",
    description="Оценка рецензии на фильм",
    response_description="Оценка",
    tags=["reviews"],
    dependencies=[Depends(JWTBearer())]
)
async def score_review(request: Request):
    return ""


@router.get(
    "/reviews",
    response_model=None,
    summary="Получение списка рецензий",
    description="Получение списка рецензий с возможностью гибкой сортировки",
    response_description="Список рецензий",
    tags=["reviews"],
    dependencies=[Depends(JWTBearer())]
)
async def get_reviews(request: Request):
    return ""