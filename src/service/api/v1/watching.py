import logging
import uuid
from uuid import UUID

from aiokafka import AIOKafkaProducer
from api.v1.schemas import WatchingResponse
from auth.auth_bearer import JWTBearer
from auth.auth_handler import decode_jwt, encode_jwt
from db.kafka import get_kafka_producer
from fastapi import APIRouter, Depends, Request

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "/{movie_id}",
    response_model=WatchingResponse,
    summary="Добавление просмотренного фрейма в кафку",
    description="",
    dependencies=[Depends(JWTBearer())],
)
async def watched_movies(
    request: Request,
    frame: str,
    movie_id: UUID,
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    user = request.state.user_id
    await kafka_producer.send_and_wait(f"{user}{movie_id}", frame.encode("UTF-8"))
    return WatchingResponse(movie_id=movie_id, user_id=user, frame=frame)


@router.get(
    "/access_token",
    response_model=None,
    summary="",
    description="",
    response_description="",
)
async def get_access_token(user_id: str | None = None) -> str:
    if not user_id:
        user_id = str(uuid.uuid4())
    token: str = encode_jwt(user_id)
    return token
