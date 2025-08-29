from abc import ABC, abstractmethod
from typing import Any


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict[str, Any]):
        raise NotImplementedError

    async def get_all(self):
        raise NotImplementedError

    async def edit_one(self, id: int, data: dict[str, Any]):
        raise NotImplementedError

    async def get_one(self, id: int):
        raise NotImplementedError

    async def delete_one(self, id: int):
        raise NotImplementedError

    async def find_all(self, **filter_by):
        raise NotImplementedError
