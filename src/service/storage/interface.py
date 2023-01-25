from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List


T = TypeVar("T")


class Storage(ABC, Generic[T]):
    @abstractmethod
    async def insert(self, item: T) -> None:
        pass

    @abstractmethod
    async def insert_chunk(self, items: List[T], **kwargs) -> None:
        pass

    @abstractmethod
    async def select(self, id: str) -> T:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    async def update(self, id: T) -> bool:
        pass

    @abstractmethod
    async def select_items(self, query: str, fltr: dict, **kwargs) -> List[T]:
        pass
