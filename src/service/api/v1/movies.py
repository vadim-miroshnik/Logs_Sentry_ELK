from http import HTTPStatus
from uuid import UUID
import json
from bson import json_util
from fastapi import APIRouter, Depends, HTTPException, Query, Header, Request, Body
from auth.auth_bearer import JWTBearer
from .schemas import ScoreResponse
from db.kafka_service import get_kafka_service
from storage.kafka import KafkaService

router = APIRouter()


@router.post(
    "/add-score",
    responses={
        int(HTTPStatus.CREATED): {
            "model": ScoreResponse,
            "description": "Successful Response",
        },
    },
    summary="Добавление оценки к фильму",
    description="Добавление/изменение/удаление оценки к фильму",
    tags=["movies"],
    dependencies=[Depends(JWTBearer())],
)
async def add_score(
    request: Request,
    movie_id: UUID = Body(default=None),
    score: int = Body(default=None),
    kafka: KafkaService = Depends(get_kafka_service)
):
    user = request.state.user_id
    data = {
        "user_id": user,
        "movie_id": movie_id,
        "score": score,
    }
    kafka.send(
        "reviews",
        f"{user}+{movie_id}",
        json.dumps(data, default=json_util.default).encode("utf-8"),
    )
    return ScoreResponse(
        user_id=user,
        movie_id=movie_id,
        score=score
    )


@router.patch(
    "/update-score",
    responses={
        int(HTTPStatus.CREATED): {
            "model": ScoreResponse,
            "description": "Successful Response",
        },
    },
    summary="Добавление оценки к фильму",
    description="Добавление/изменение/удаление оценки к фильму",
    tags=["movies"],
    dependencies=[Depends(JWTBearer())],
)
async def update_score(
    request: Request,
    movie_id: UUID = Body(default=None),
    score: int = Body(default=None),
    kafka: KafkaService = Depends(get_kafka_service)
):
    user = request.state.user_id
    data = {
        "user_id": user,
        "movie_id": movie_id,
        "score": score,
    }
    kafka.send(
        "reviews",
        f"{user}+{movie_id}",
        json.dumps(data, default=json_util.default).encode("utf-8"),
    )
    return ScoreResponse(
        user_id=user,
        movie_id=movie_id,
        score=score
    )


@router.delete(
    "/",
    responses={
        int(HTTPStatus.NO_CONTENT): {
            "model": None,
            "description": "Successful Response",
        },
    },
    summary="Удаление оценки",
    tags=["movies"],
    dependencies=[Depends(JWTBearer())]
)
async def delete_score(
    request: Request,
    movie_id: UUID = Body(default=None),
    kafka: KafkaService = Depends(get_kafka_service)
) -> None:
    user = request.state.user_id
    await kafka.send(
        "movies",
        f"{user}+{movie_id}",
        "0",
    )


@router.get(
    "/scores",
    response_model=list[ScoreResponse],
    summary="Получение оценки фильма",
    description="Получение средней оценки фильма, количество лайков/дизлайков",
    response_description="Оценка фильма",
    tags=["movies"],
    dependencies=[Depends(JWTBearer())],
)
async def get_score(
    request: Request,
    movie_id: UUID = Body(default=None)
) -> list[ScoreResponse]:
    user = request.state.user_id
    return None
