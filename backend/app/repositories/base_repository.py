import itertools
from typing import Type

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AbstractModel


class BaseRepository[TModel: AbstractModel]:
    def __init__(self, session: AsyncSession, model: Type[TModel]):
        self.__session = session
        self.__model = model

    async def get(self, model_id: int) -> TModel | None:
        query = select(self.__model).filter_by(id=model_id)
        result = await self.__session.execute(query)
        return result.scalar_one_or_none()

    async def add(self, model: TModel) -> TModel:
        self.__session.add(model)
        await self.__session.flush()
        return model

    async def update(self, model_id: int, model: TModel) -> int:
        query = update(self.__model).where(self.__model.id == model_id).values(**model.model_dump(exclude_unset=True))
        result = await self.__session.execute(query)
        await self.__session.flush()
        return result.rowcount()

    async def delete(self, model_id: int):
        obj = await self.get(model_id)
        await self.__session.delete(obj)
        await self.__session.flush()
        return obj

    async def get_all(self):
        query = select(self.__model)
        result = await self.__session.execute(query)
        return tuple(itertools.chain.from_iterable(result.all()))