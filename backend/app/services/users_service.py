from typing import Type, List, Any

from fastapi import HTTPException, status

from app.common.security import get_password_hash
from app.repositories import SQLAlchemyRepository
from app.schemas.user_schemas import UserCreateSchema, UserReadSchema


class UsersService:
    def __init__(self, users_repo: Type[SQLAlchemyRepository]):
        self.users_repo: SQLAlchemyRepository = users_repo()

    async def add_user(self, user: UserCreateSchema) -> UserReadSchema:
        user_dict = user.model_dump()

        if not await self.__check_email_unique(user_dict):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already used")

        user_dict = self.__encrypt_user_password(user_dict)
        user_id = await self.users_repo.add_one(user_dict)
        user = await self.users_repo.get_one(user_id)
        return user

    async def get_users(self) -> List[UserReadSchema]:
        users = await self.users_repo.get_all()
        return users

    async def get_user(self, id: int) -> UserReadSchema:
        user = await self.users_repo.get_one(id)
        return user

    async def __check_email_unique(self, user_dict: dict[str, Any]) -> bool:
        users = await self.users_repo.find_all(email=user_dict["email"])
        return len(users) == 0

    @classmethod
    def __encrypt_user_password(cls, user_dict: dict[str, Any]) -> dict[str, Any]:
        user_dict["hashed_password"] = get_password_hash(user_dict["password"])
        del user_dict["password"]
        return user_dict
