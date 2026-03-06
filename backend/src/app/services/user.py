from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repositories import UserRepository


class UserService:
    def __init__(self, db_session: AsyncSession):
        self.__user_repository = UserRepository(db_session)

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        users = await self.__user_repository.find_all(id=user_id)
        if len(users) > 0:
            return users.pop()
        return None
