from typing import List

from sqlalchemy import insert, select, update, delete

from app.db.session import async_session_maker
from app.schemas.base_schemas import BaseReadSchema
from .abstract_repository import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def edit_one(self, id: int, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_all(self) -> List[BaseReadSchema]:
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            res = [row[0].to_read_schema() for row in res.all()]
            return res

    async def get_one(self, id: int) -> BaseReadSchema:
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(id=id)
            res = await session.execute(stmt)
            res = res.scalar_one().to_read_schema()
            return res

    async def delete_one(self, id: int) -> int:
        async with async_session_maker() as session:
            stmt = delete(self.model).filter_by(id=id).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_all(self, **filter_by) -> list[BaseReadSchema]:
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            res = [row[0].to_read_schema() for row in res.all()]
            return res
