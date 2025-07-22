from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repositories import UserRepository
from app.schemas import UserCreateSchema, UserSchema


class UserService:
    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__user_repository = UserRepository(session)

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.__user_repository.get(user_id)
        if user is None:
            raise HTTPException(status_code=404)
        return user

    async def create_user(self, user_data: UserCreateSchema) -> User:
        user = User(**user_data.model_dump(exclude_unset=True))
        await self.__user_repository.add(user_data)

    async def update_user(self, user_id: int, user_data: UserSchema) -> User:
        pass

    async def delete_user(self, user_id: int):
        pass
