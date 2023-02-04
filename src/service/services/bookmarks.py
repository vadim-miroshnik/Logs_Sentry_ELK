from uuid import UUID

from storage.mongodb import Mongodb


class BookmarksService:
    def __init__(self, stor: Mongodb):
        self.stor = stor

    async def add(self, user_id: str, movie_id: str):
        bookmarks = await self.stor.select({"_id": user_id})
        if bookmarks:
            return await self.stor.update({"_id": user_id}, {"$addToSet": {"bookmarks": movie_id}})
        return await self.stor.insert({"_id": user_id, "bookmarks": [movie_id]})

    async def delete(self, user_id: str, movie_id: str):
        return await self.stor.update({"_id": user_id}, {"$pull": {"bookmarks": movie_id}})

    async def get(self, user_id: str):
        return await self.stor.select({"_id": user_id})
