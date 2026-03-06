from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session

    async def find_all(self, **filter_by) -> Sequence[User]:
        stmt = select(User).filter_by(**filter_by)
        result = await self.__db_session.execute(stmt)
        items = result.scalars().all()
        return items
