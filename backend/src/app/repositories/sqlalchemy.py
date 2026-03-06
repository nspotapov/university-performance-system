from typing import List, Type, Optional

from app.core.types import Id
from sqlalchemy import insert, select, update, delete


class SQLAlchemyRepository:
    model = None

    def __init__(self, db_session):
        self.__db_session = db_session

    async def create(self, data: dict) -> Type[model]:
        stmt = insert(self.model).values(**data)
        result = await self.__db_session.execute(stmt)
        await self.__db_session.commit()
        pk = result.lastrowid
        item = await self.read(pk)
        return item

    async def update(self, pk: int, data: dict) -> Optional[Type[model]]:
        stmt = update(self.model).values(**data).filter_by(id=pk)
        await self.__db_session.execute(stmt)
        await self.__db_session.commit()
        item = await self.read(pk)
        return item

    async def delete(self, pk: int) -> Optional[Type[model]]:
        item = await self.read(pk)
        stmt = delete(self.model).filter_by(id=pk)
        await self.__db_session.execute(stmt)
        await self.__db_session.commit()
        return item

    async def find_all(self, offset: int = 0, limit: int = 25, **filter_by) -> List[Type[model]]:
        stmt = select(self.model).filter_by(**filter_by).offset(offset).limit(limit)
        result = await self.__db_session.execute(stmt)
        items = list(result.scalars().all())
        return items

    async def read(self, pk: int) -> Optional[Type[model]]:
        items = await self.find_all(id=pk)
        if items:
            return items.pop()
