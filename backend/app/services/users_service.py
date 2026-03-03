from typing import Type, List, Any

from fastapi import HTTPException, status

from app.common import text_messages
from app.common.security import get_password_hash
from app.exceptions import ApplicationException
from app.repositories import SQLAlchemyRepository
from app.schemas.user_schemas import UserCreateSchema, UserReadSchema


class UsersService:
    def __init__(self, users_repo: Type[SQLAlchemyRepository]):
        self.users_repo: SQLAlchemyRepository = users_repo()

    async def add_user(self, user_create_schema: UserCreateSchema) -> UserReadSchema:
        user_dict = user_create_schema.model_dump()

        if not await self.__check_email_unique(user_dict):
            raise ApplicationException(text_messages.EMAIL_ALREADY_USED)

        user_dict = self.__encrypt_user_password(user_dict)
        await self.users_repo.add_one(user_dict)
        users = await self.users_repo.find_all(email=user_create_schema.email)
        user_read_schema = users[0]
        return user_read_schema

    async def get_users(self) -> List[UserReadSchema]:
        users = await self.users_repo.get_all()
        return users

    async def get_user(self, pk: str) -> UserReadSchema:
        user = await self.users_repo.get_one(pk)
        return user

    async def __check_email_unique(self, user_dict: dict[str, Any]) -> bool:
        users = await self.users_repo.find_all(email=user_dict["email"])
        return len(users) == 0

    @classmethod
    def __encrypt_user_password(cls, user_dict: dict[str, Any]) -> dict[str, Any]:
        user_dict["hashed_password"] = get_password_hash(user_dict["password"])
        del user_dict["password"]
        return user_dict
