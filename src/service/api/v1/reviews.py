import json
import uuid
from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from auth.auth_bearer import JWTBearer
from bson import json_util
from db.kafka_service import get_kafka_service
from db.mongodb import get_mongodb_reviews
from fastapi import (APIRouter, Body, Depends, Header, HTTPException, Query,
                     Request)
from services.reviews import ReviewsService
from storage.kafka import KafkaService

from .schemas import ReviewResponse

router = APIRouter()


@router.post(
    "/add",
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
    movie_id: UUID = Query(default=uuid.uuid4()),
    text: str = Query(default=None),
    score: int = Query(default=None),
    kafka: KafkaService = Depends(get_kafka_service),
    service: ReviewsService = Depends(get_mongodb_reviews),
):
    user = request.state.user_id
    await service.add(user, str(movie_id), text)
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
    "/update",
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
    review_id: UUID = Query(default=uuid.uuid4()),
    text: str = Query(default=None),
    score: int = Query(default=None),
    kafka: KafkaService = Depends(get_kafka_service),
    service: ReviewsService = Depends(get_mongodb_reviews),
) -> ReviewResponse:
    user = request.state.user_id
    await service.update(str(review_id), text)
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
        review_id=data["review_id"],
        text=text,
        score=score,
        pub_dt=data["pub_dt"],
    )


@router.post(
    "/add-score",
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
    review_id: UUID = Query(default=uuid.uuid4()),
    score: int = Query(default=None),
    kafka: KafkaService = Depends(get_kafka_service),
    service: ReviewsService = Depends(get_mongodb_reviews),
) -> ReviewResponse:
    user = request.state.user_id
    await service.add_score(str(review_id), user, score)
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
        review_id=data["review_id"],
        score=score,
    )


@router.delete(
    "/del-score",
    responses={
        int(HTTPStatus.NO_CONTENT): {
            "model": None,
            "description": "Successful Response",
        },
    },
    summary="Удаление оценки рецензии на фильм",
    description="Удаление оценки рецензии на фильм",
    tags=["reviews"],
    dependencies=[Depends(JWTBearer())],
)
async def del_score_review(
    request: Request,
    review_id: UUID = Query(default=uuid.uuid4()),
    kafka: KafkaService = Depends(get_kafka_service),
    service: ReviewsService = Depends(get_mongodb_reviews),
) -> None:
    user = request.state.user_id
    await service.del_score(str(review_id), user)
    data = {
        "review_id": uuid.uuid4(),
        "score": 0,
    }
    kafka.send(
        "reviews",
        f"{review_id}",
        json.dumps(data, default=json_util.default).encode("utf-8"),
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
    description="Получение списка рецензий",
    tags=["reviews"],
    # dependencies=[Depends(JWTBearer())],
)
async def get_reviews(
    request: Request,
    movie_id: UUID = Query(default=uuid.uuid4()),
    service: ReviewsService = Depends(get_mongodb_reviews),
) -> list[ReviewResponse]:
    user = request.state.user_id
    return await service.get(movie_id)
