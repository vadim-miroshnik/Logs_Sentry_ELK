import json
import uuid
from http import HTTPStatus
from uuid import UUID

from auth.auth_bearer import auth
from bson import json_util
from db.kafka_service import get_kafka_service
from db.mongodb import get_mongodb_bookmarks
from fastapi import APIRouter, Body, Depends, Header, HTTPException, Query, Request
from services.bookmarks import BookmarksService
from storage.kafka import KafkaService

from .schemas import BookmarkResponse

router = APIRouter()


@router.post(
    "/add",
    responses={
        int(HTTPStatus.CREATED): {
            "model": BookmarkResponse,
            "description": "Successful Response",
        },
    },
    summary="Добавление закладки на фильм",
    description="Добавление закладки на фильм",
    tags=["bookmarks"],
    dependencies=[Depends(auth)],
)
async def add_bookmark(
    request: Request,
    movie_id: UUID = Query(default=uuid.uuid4()),
    kafka: KafkaService = Depends(get_kafka_service),
    service: BookmarksService = Depends(get_mongodb_bookmarks),
) -> BookmarkResponse:
    user = request.state.user_id
    await service.add(user, str(movie_id))
    await kafka.send(
        "bookmarks",
        f"{user}+{movie_id}",
        "1".encode("utf-8"),
    )
    return BookmarkResponse(
        user_id=user,
        movie_id=movie_id,
    )


@router.get(
    "/get",
    responses={
        int(HTTPStatus.OK): {
            "model": list[BookmarkResponse],
            "description": "Successful Response",
        },
    },
    summary="Получение закладок на фильмы",
    description="Получение закладок на фильмы",
    tags=["bookmarks"],
    dependencies=[Depends(auth)],
)
async def get_bookmark(
    request: Request, service: BookmarksService = Depends(get_mongodb_bookmarks)
) -> list[BookmarkResponse]:
    user = request.state.user_id
    return await service.get(user)


@router.delete(
    "/delete",
    responses={
        int(HTTPStatus.NO_CONTENT): {
            "model": None,
            "description": "Successful Response",
        },
    },
    summary="Удаление закладки",
    tags=["bookmarks"],
    dependencies=[Depends(auth)],
)
async def delete_bookmark(
    request: Request,
    movie_id: UUID = Query(default=uuid.uuid4()),
    kafka: KafkaService = Depends(get_kafka_service),
    service: BookmarksService = Depends(get_mongodb_bookmarks),
) -> None:
    user = request.state.user_id
    await kafka.send(
        "bookmarks",
        f"{user}+{movie_id}",
        "0".encode("utf-8"),
    )
    await service.delete(user, str(movie_id))
