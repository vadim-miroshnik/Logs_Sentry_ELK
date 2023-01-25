from http import HTTPStatus

import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, Header, Request
from models.events import ViewEvent
from storage.mongodb import Mongodb
from db.mongodb import get_mongodb_view_events


router = APIRouter()


@router.post(
    "/test",
    response_model=None,
    summary="",
    description="",
    response_description="",
    tags=["events"],
)
async def test(request: Request, stor: Mongodb[ViewEvent] = Depends(get_mongodb_view_events)
) -> str:
    event: ViewEvent = ViewEvent(user_id='test', movie_id='test', viewed_frame=100)
    await stor.insert(event)
    await stor.select("test")
    return ""