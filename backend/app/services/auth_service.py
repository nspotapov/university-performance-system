from typing import Type

from app.common.security import get_password_hash, verify_password
from app.repositories import SQLAlchemyRepository
from app.schemas.auth_schemas import AuthLoginRequestSchema
from app.schemas.user_schemas import UserReadSchema


class AuthService:
    def __init__(self, users_repo: Type[SQLAlchemyRepository]):
        self.users_repo: SQLAlchemyRepository = users_repo()

    async def login_user(self, schema: AuthLoginRequestSchema) -> UserReadSchema | None:
        users = await self.users_repo.find_all(email=schema.email)

        if len(users) == 0:
            return None

        user = users[0]

        if not verify_password(schema.password, user.hashed_password):
            return None

        return user
