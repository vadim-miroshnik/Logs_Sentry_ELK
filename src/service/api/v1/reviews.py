import uuid
from http import HTTPStatus
from uuid import UUID
from datetime import datetime
import json
from bson import json_util

from fastapi import APIRouter, Depends, HTTPException, Query, Header, Request, Body
from auth.auth_bearer import JWTBearer
from .schemas import ReviewResponse
from storage.kafka import KafkaService
from db.kafka_service import get_kafka_service

router = APIRouter()


@router.post(
    "/add-review",
    responses={
        int(HTTPStatus.CREATED): {
            "model": ReviewResponse,
            "description": "Successful Response",
        },
    },
    summary="Создание рецензии на фильм",
    description="При создании рецензии передается текст, дата публикации и оценка фильма",
    tags=["reviews"],
    dependencies=[Depends(JWTBearer())],
)
async def add_review(
    request: Request,
    movie_id: UUID = Body(default=None),
    text: str = Body(default=None),
    score: int = Body(default=None),
    kafka: KafkaService = Depends(get_kafka_service),
):
    user = request.state.user_id
    data = {
        "user_id": user,
        "review_id": str(uuid.uuid4()),
        "movie_id": str(movie_id),
        "text": text,
        "pub_dt": datetime.now(),
        "score": score,
    }
    await kafka.send(
        "reviews",
        f"{user}+{movie_id}",
        json.dumps(data, default=json_util.default).encode("utf-8"),
    )
    return ReviewResponse(
        user_id=user,
        review_id=data["review_id"],
        movie_id=movie_id,
        text=text,
        score=score,
        pub_dt=data["pub_dt"],
    )


@router.patch(
    "/update-review",
    responses={
        int(HTTPStatus.CREATED): {
            "model": ReviewResponse,
            "description": "Successful Response",
        },
    },
    summary="Обновление рецензии на фильм",
    description="При обновлении рецензии передается текст, дата публикации и оценка фильма",
    tags=["reviews"],
    dependencies=[Depends(JWTBearer())],
)
async def update_review(
    request: Request,
    review_id: UUID = Body(default=None),
    text: str = Body(default=None),
    score: int = Body(default=None),
    kafka: KafkaService = Depends(get_kafka_service),
):
    user = request.state.user_id
    data = {
        "user_id": user,
        "review_id": review_id,
        "text": text,
        "pub_dt": datetime.now(),
        "score": score,
    }
    kafka.send(
        "reviews",
        f"{review_id}",
        json.dumps(data, default=json_util.default).encode("utf-8"),
    )
    return ReviewResponse(
        user_id=user,
        review_id=data.review_id,
        movie_id="", # movie_id,
        text=text,
        score=score,
        pub_dt=data.pub_dt,
    )


@router.post(
    "/score-review",
    responses={
        int(HTTPStatus.CREATED): {
            "model": ReviewResponse,
            "description": "Successful Response",
        },
    },
    summary="Оценка рецензии на фильм",
    description="Оценка рецензии на фильм",
    tags=["reviews"],
    dependencies=[Depends(JWTBearer())],
)
async def score_review(
    request: Request,
    review_id: UUID = Body(default=None),
    score: int = Body(default=None),
    kafka: KafkaService = Depends(get_kafka_service)
):
    user = request.state.user_id
    data = {
        "review_id": uuid.uuid4(),
        "score": score,
    }
    kafka.send(
        "reviews",
        f"{review_id}",
        json.dumps(data, default=json_util.default).encode("utf-8"),
    )
    return ReviewResponse(
        user_id=user,
        review_id=data.review_id,
        score=score,
    )


@router.get(
    "/reviews",
    responses={
        int(HTTPStatus.CREATED): {
            "model": list[ReviewResponse],
            "description": "Successful Response",
        },
    },
    summary="Получение списка рецензий",
    description="Получение списка рецензий с возможностью гибкой сортировки",
    tags=["reviews"],
    dependencies=[Depends(JWTBearer())],
)
async def get_reviews(
    request: Request,
    movie_id: UUID = Body(default=None)
):
    user = request.state.user_id
    return None
