import datetime
import uuid

from storage.mongodb import Mongodb


class ReviewsService:
    def __init__(self, stor: Mongodb):
        self.stor = stor

    async def add(self, user_id: str, movie_id: str, text: str):
        review = await self.stor.select({"user_id": user_id, "movie_id": movie_id})
        if review:
            return await self.stor.update(
                {"_id": review["_id"]},
                {"$set": {"text": text, "pub_dt": datetime.datetime.now()}},
            )
        return await self.stor.insert(
            {
                "_id": str(uuid.uuid4()),
                "movie_id": movie_id,
                "user_id": user_id,
                "text": text,
                "pub_dt": datetime.datetime.now(),
                "scores": [],
            }
        )

    async def update(self, review_id: str, text: str):
        review = await self.stor.select({"_id": review_id})
        if review:
            return await self.stor.update(
                {"_id": review_id},
                {"$set": {"text": text, "pub_dt": datetime.datetime.now()}},
            )
        return None

    async def add_score(self, review_id: str, user_id: str, score: int):
        review = await self.stor.select({"_id": review_id})
        if review:
            return await self.stor.update(
                {"_id": review_id},
                {"$addToSet": {"scores": {"user_id": user_id, "score": score}}},
            )
        return None

    async def del_score(self, review_id: str, user_id: str):
        review = await self.stor.select({"_id": review_id})
        if review:
            return await self.stor.update(
                {"_id": review_id}, {"$pull": {"scores": {"user_id": user_id}}}
            )
        return None

    async def get(self, movie_id: str):
        reviews = await self.stor.select_items({"movie_id": movie_id})
        return reviews
