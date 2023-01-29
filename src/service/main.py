import asyncio

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.openapi.utils import get_openapi
import pymongo

from api.v1 import watching, reviews, movies, bookmarks
from core.config import settings
from db import kafka, mongodb

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    swagger_ui_parameters={"syntaxHighlight": False}
)

def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=settings.project_name,
            version="1.0.0",
            openapi_version="3.0.0",
            description="",
            routes=app.routes,
            tags="",
            servers="",
        )
        for _, method_item in app.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                if '422' in responses:
                    del responses['422']
                if '200' in responses:
                    del responses['200']
    return app.openapi_schema


app.openapi = custom_openapi


@app.on_event("startup")
async def startup_event():
    kafka.producer = AIOKafkaProducer(bootstrap_servers=f"{settings.kafka.host}:{settings.kafka.port}")
    await kafka.producer.start()

    # mongodb.mongodb = pymongo.MongoClient(
    #    "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000")


@app.on_event("shutdown")
async def shutdown_event():
    await kafka.producer.stop()

    await mongodb.mongodb.close()


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
