import asyncio

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import watching
from core.config import settings
from db import kafka

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup_event():
    kafka.producer = AIOKafkaProducer(bootstrap_servers=f"{settings.kafka.host}:{settings.kafka.port}")
    await kafka.producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka.producer.stop()


app.include_router(watching.router, prefix="/api/v1/watching", tags=["films"])

if __name__ == "__main__":
    uvicorn.run(
        app,  # type: ignore
        host="0.0.0.0",
        port=8000,
    )
