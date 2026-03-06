from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repositories import UserRepository


class UserService:
    def __init__(self, db_session: AsyncSession):
        self.__user_repository = UserRepository(db_session)

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        user = await self.__user_repository.read(user_id)
        return user
