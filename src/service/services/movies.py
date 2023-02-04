from storage.mongodb import Mongodb


class MoviesService:
    def __init__(self, stor: Mongodb):
        self.stor = stor

    async def add(self, user_id: str, movie_id: str, score: int):
        movie = await self.stor.select({"_id": movie_id})
        if movie:
            score_cnt = len(movie["scores"])
            rating = (movie.get("rating") * score_cnt + score) / (score_cnt + 1)
            await self.stor.update({"_id": movie_id}, {"$set": {"rating": rating}})
            return await self.stor.update(
                {"_id": movie_id},
                {"$addToSet": {"scores": {"user_id": user_id, "score": score}}},
            )
        return await self.stor.insert(
            {
                "_id": movie_id,
                "scores": [{"user_id": user_id, "score": score}],
                "rating": score,
            }
        )

    async def update(self, user_id: str, movie_id: str, score: int):
        movie = await self.stor.select({"_id": movie_id})
        if movie:
            old_score = next(score for score in movie["scores"] if score["user_id"] == user_id).get("score")
            score_cnt = len(movie["scores"])
            rating = (movie["rating"] + score - old_score) / score_cnt
            await self.stor.update({"_id": movie_id}, {"$set": {"rating": rating}})
            return await self.stor.update(
                {"_id": movie_id, "scores.user_id": user_id},
                {"$set": {"scores.$.score": score}},
            )
        return None

    async def delete(self, user_id: str, movie_id: str):
        movie = await self.stor.select({"_id": movie_id})
        if movie:
            score_cnt = len(movie["scores"])
            score = next(score for score in movie["scores"] if score["user_id"] == user_id).get("score")
            rating = (movie["rating"] * score_cnt - score) / (score_cnt - 1)
            await self.stor.update({"_id": movie_id}, {"$set": {"rating": rating}})
            return await self.stor.update({"_id": movie_id}, {"$pull": {"scores": {"user_id": user_id}}})
        return None

    async def get(self, movie_id: str):
        movie = await self.stor.select({"_id": movie_id})
        if movie:
            return {"scores": len(movie["scores"]), "rating": movie["rating"]}
        return None
