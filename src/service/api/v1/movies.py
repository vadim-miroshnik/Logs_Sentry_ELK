from http import HTTPStatus
import uuid
from uuid import UUID
import json
from bson import json_util
from fastapi import APIRouter, Depends, HTTPException, Query, Header, Request, Body
from auth.auth_bearer import JWTBearer
from .schemas import ScoreResponse
from db.kafka_service import get_kafka_service
from storage.kafka import KafkaService
from services.movies import MoviesService
from db.mongodb import get_mongodb_movies

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
    movie_id: UUID = Query(default=uuid.uuid4()),
    score: int = Query(default=None),
    kafka: KafkaService = Depends(get_kafka_service),
    service: MoviesService = Depends(get_mongodb_movies)
) -> ScoreResponse:
    user = request.state.user_id
    await service.add(user, str(movie_id), score)
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
    movie_id: UUID = Query(default=uuid.uuid4()),
    score: int = Query(default=None),
    kafka: KafkaService = Depends(get_kafka_service),
    service: MoviesService = Depends(get_mongodb_movies)
):
    user = request.state.user_id
    await service.update(user, str(movie_id), score)
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
    movie_id: UUID = Query(default=uuid.uuid4()),
    kafka: KafkaService = Depends(get_kafka_service),
    service: MoviesService = Depends(get_mongodb_movies)
) -> None:
    user = request.state.user_id
    await service.delete(user, str(movie_id))
    await kafka.send(
        "movies",
        f"{user}+{movie_id}",
        "0",
    )


@router.get(
    "/scores",
    response_model=ScoreResponse,
    summary="Получение оценки фильма",
    description="Получение средней оценки фильма, количество лайков/дизлайков",
    response_description="Оценка фильма",
    tags=["movies"],
    dependencies=[Depends(JWTBearer())],
)
async def get_score(
    request: Request,
    movie_id: UUID = Query(default=uuid.uuid4()),
    service: MoviesService = Depends(get_mongodb_movies)
) -> ScoreResponse:
    user = request.state.user_id
    res = await service.get(str(movie_id))
    return ScoreResponse(
        user_id=user,
        movie_id=movie_id,
        score=res.get("scores"),
        avg_score=res.get("rating")
    )
