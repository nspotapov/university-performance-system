from typing import List, Optional, Generic, TypeVar, Type, Tuple

from sqlalchemy import insert, select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class SQLAlchemyRepository(Generic[T]):
    model: Type[T] = None

    def __init__(self, db_session: AsyncSession):
        self._session = db_session

    async def create(self, data: dict) -> T:
        # Сразу возвращаем созданный объект
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def update(self, pk: int, data: dict) -> Optional[T]:
        stmt = (
            update(self.model)
            .filter_by(id=pk)
            .values(**data)
            .returning(self.model)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, pk: int) -> Optional[T]:
        stmt = delete(self.model).filter_by(id=pk).returning(self.model)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def read(self, pk: int) -> Optional[T]:
        stmt = select(self.model).filter_by(id=pk)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_all(self, size: int = 50, page: int = 1, **filter_by) -> Tuple[List[T], int]:
        stmt = (
            select(self.model)
            .filter_by(**filter_by)
            .offset((page - 1) * size)
            .limit(size)
        )
        result = await self._session.execute(stmt)
        items = list(result.scalars())
        total = await self.count(**filter_by)
        return items, total

    async def count(self, **filter_by) -> int:
        stmt = select(func.count()).select_from(self.model).filter_by(**filter_by)
        result = await self._session.execute(stmt)
        return result.scalar() or 0
