from typing import Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas import Page
from app.api.v1.users.schemas import UserReadResponseSchema, UserCreateRequestSchema, UserUpdateRequestSchema
from app.core import messages
from app.core.exceptions import ApplicationException
from app.core.security import get_password_hash
from app.repositories import UserRepository


class UserService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__user_repository = UserRepository(db_session)

    async def get_user(self, user_id: int) -> Optional[UserReadResponseSchema]:
        user_model = await self.__user_repository.read(user_id)
        if user_model is None:
            raise ApplicationException(messages.ERROR_USER_NOT_FOUND)
        return UserReadResponseSchema.model_validate(user_model)

    async def get_users(self, size: int = 50, page: int = 1) -> Page[UserReadResponseSchema]:
        users, total = await self.__user_repository.find_all(size=size, page=page)
        return Page[UserReadResponseSchema](
            items=[UserReadResponseSchema.model_validate(user_model) for user_model in users],
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

    async def create_user(self, user_schema: UserCreateRequestSchema) -> UserReadResponseSchema:
        if not await self.__is_email_unique(str(user_schema.email)):
            raise ApplicationException(messages.ERROR_EMAIL_ALREADY_USED)
        user_data = self.__encrypt_user_password(user_schema.model_dump())
        user_model = await self.__user_repository.create(user_data)
        await self.__db_session.commit()
        return UserReadResponseSchema.model_validate(user_model)

    async def update_user(
            self,
            user_id: int,
            user_schema: UserUpdateRequestSchema
    ) -> UserReadResponseSchema:
        if not await self.__is_email_unique(str(user_schema.email), user_id):
            raise ApplicationException(messages.ERROR_EMAIL_ALREADY_USED)
        user_data = self.__encrypt_user_password(user_schema.model_dump(exclude_unset=True))
        user_model = await self.__user_repository.update(user_id, user_data)
        if user_model is None:
            raise ApplicationException(messages.ERROR_USER_NOT_FOUND)
        await self.__db_session.commit()
        return UserReadResponseSchema.model_validate(user_model)

    async def delete_user(self, user_id: int) -> UserReadResponseSchema:
        user_model = await self.__user_repository.delete(user_id)
        if user_model is None:
            raise ApplicationException(messages.ERROR_USER_NOT_FOUND)
        await self.__db_session.commit()
        return UserReadResponseSchema.model_validate(user_model)

    async def __is_email_unique(self, email: str, user_id: int = None) -> bool:
        users, _ = await self.__user_repository.find_all(email=email)
        if not users:
            return True
        user = users.pop()
        return user.id == user_id

    @classmethod
    def __encrypt_user_password(cls, user_data: dict[str, Any]) -> dict[str, Any]:
        if "password" in user_data:
            user_data["hashed_password"] = get_password_hash(user_data["password"])
            del user_data["password"]
        return user_data
