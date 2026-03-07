from typing import Annotated, List

from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.users.schemas import UserReadResponseSchema
from app.core import messages
from app.core.security import jwt_security
from app.db.session import get_async_session
from app.models import UserRole
from app.services import UserService, AuthService


async def get_auth_service(db_session: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(db_session)


async def get_user_service(db_session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(db_session)


async def get_current_user(
        request: Request,
        user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadResponseSchema:
    # Get access token from HEADERS only (not cookies)
    access_token = await jwt_security.get_access_token_from_request(
        request,
        locations=["headers"],  # Only look in headers
    )
    # Verify the access token
    # No CSRF verification needed for header-based tokens
    access_token_payload = jwt_security.verify_token(access_token, verify_csrf=False)
    return await user_service.get_user(int(access_token_payload.sub))


def check_user_role(roles: List[UserRole]):
    def role_checker(
            current_user: Annotated[UserReadResponseSchema, Depends(get_current_user)]) -> UserReadResponseSchema:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail=messages.ERROR_USER_HAVE_NOT_ENOUGH_RIGHTS
            )
        return current_user

    return role_checker


__all__ = (
    "get_auth_service",
    "get_user_service",
    "check_user_role",
    "get_current_user",
)
