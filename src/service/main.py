import asyncio

import uvicorn
from aiokafka import AIOKafkaProducer
import aioredis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import watching, reviews, movies, bookmarks
from core.config import settings
from db import kafka
from db import redis

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    swagger_ui_parameters={"syntaxHighlight": False}
)


@app.on_event("startup")
async def startup_event():
    kafka.producer = AIOKafkaProducer(bootstrap_servers=f"{settings.kafka.host}:{settings.kafka.port}")
    await kafka.producer.start()

    redis.redis = await aioredis.create_redis_pool(
        address=(settings.redis.host, settings.redis.port), minsize=10, maxsize=20
    )


@app.on_event("shutdown")
async def shutdown_event():
    await kafka.producer.stop()

    redis.redis.close()
    await redis.redis.wait_closed()


app.include_router(watching.router, prefix="/api/v1/watching", tags=["films"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])
app.include_router(movies.router, prefix="/api/v1/movies", tags=["movies"])
app.include_router(bookmarks.router, prefix="/api/v1/bookmarks", tags=["bookmarks"])

if __name__ == "__main__":
    uvicorn.run(
        app,  # type: ignore
        host="0.0.0.0",
        port=8000,
    )
