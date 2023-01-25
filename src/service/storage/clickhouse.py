from typing import Generic, List, cast, Type, Tuple
from .interface import Storage, T
import clickhouse_driver
import datetime

class Clickhouse(Generic[T], Storage[T]):

    def __init__(self, clickhouse: clickhouse_driver.Client):
        self.clickhouse = clickhouse
        self.db = "movies"

        cls = cast(Clickhouse, self.__class__)
        if cls.__args:
            self.ref = cls.__args[0]

        self.coll = self.ref.__name__.lower()
        print(self.coll)

    def __class_getitem__(cls, *args) -> Type["Clickhouse"]:
        cls.__args = cast(Tuple[Type[T]], args)
        return super().__class_getitem__(*args)

    async def insert(self, item: T) -> None:
        try:
            print(self.clickhouse)
            self.clickhouse.execute(f'INSERT INTO analysis.views VALUES', [{
                'id': 1,
                'user_id': '',
                'movie_id': '',
                'viewed_frame': 1,
                'event_time': datetime.datetime.now()
            }])
        except clickhouse_driver.errors.Error as e:
            print(f"insert error {e.code} - {e.message}")

    async def insert_chunk(self, items: List[T], **kwargs) -> None:
        pass

    async def select(self, id: str) -> T:
        pass

    async def delete(self, id: str) -> bool:
        pass

    async def update(self, id: T) -> bool:
        pass

    async def select_items(self, query: str, fltr: dict, **kwargs) -> List[T]:
        pass

