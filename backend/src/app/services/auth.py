from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.models import User, MFAMethod
from app.repositories import UserRepository


class AuthService:
    def __init__(self, db_session: AsyncSession):
        self.user_repository = UserRepository(db_session)

    async def login_user(self, username: str, password: str) -> Optional[User]:
        users = await self.user_repository.find_all(email=username)
        if not users:
            return None
        user = users.pop()
        password_valid, _ = verify_password(password, user.hashed_password)
        if not password_valid:
            return None
        return user

    async def verify_totp_code(self, user: User, code: str) -> bool:
        pass

    async def check_mfa_enabled(self, user: User) -> bool:
        return user.is_mfa_enabled

    async def get_user_mfa_method(self, user: User) -> MFAMethod:
        return user.mfa_method

    async def check_totp_enabled(self, user: User) -> bool:
        return user.is_mfa_enabled and user.mfa_method == MFAMethod.TOTP

    async def check_user_is_active(self, user: User) -> bool:
        return user.is_active
