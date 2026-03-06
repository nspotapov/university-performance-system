from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.services import UserService, AuthService


async def get_auth_service(db_session: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(db_session)


async def get_user_service(db_session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(db_session)


__all__ = (
    "get_auth_service",
    "get_user_service",
)
