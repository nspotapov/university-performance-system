from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.users.schemas import UserReadResponseSchema
from app.core.security import verify_password, verify_totp_code
from app.models import User, MFAMethod
from app.repositories import UserRepository


class AuthService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__user_repository = UserRepository(db_session)

    async def login_user(self, username: str, password: str) -> Optional[UserReadResponseSchema]:
        users, _ = await self.__user_repository.find_all(email=username)
        if users:
            user = users.pop()
            password_valid = verify_password(password, user.hashed_password)
            if password_valid:
                return UserReadResponseSchema.model_validate(user)

    async def verify_totp_code(self, user: UserReadResponseSchema, code: str) -> bool:
        return verify_totp_code(user.totp_secret, code)

    async def check_mfa_enabled(self, user: UserReadResponseSchema) -> bool:
        return user.is_mfa_enabled

    async def get_user_mfa_method(self, user: UserReadResponseSchema) -> MFAMethod:
        return user.mfa_method

    async def check_totp_enabled(self, user: UserReadResponseSchema) -> bool:
        return user.is_mfa_enabled and user.mfa_method == MFAMethod.TOTP

    async def check_user_is_active(self, user: UserReadResponseSchema) -> bool:
        return user.is_active
