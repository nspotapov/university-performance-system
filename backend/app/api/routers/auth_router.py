from typing import Annotated

from authx import TokenPayload
from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.api.dependencies import get_auth_manager, get_users_service
from app.common.security import jwt_security
from app.managers.auth_manager import AuthManager
from app.schemas.auth_schemas import AuthLoginSchema, AuthOTPLoginSchema
from app.services import UsersService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login")
async def login_user(
        schema: AuthLoginSchema,
        auth_manager: Annotated[AuthManager, Depends(get_auth_manager)],
):
    user = await auth_manager.login_user(schema)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return {"status": "success", "detail": "Код подтверждения выслан на указанную вами почту"}


@router.post("/otp")
async def login_user(
        schema: AuthOTPLoginSchema,
        auth_manager: Annotated[AuthManager, Depends(get_auth_manager)],
        response: Response
):
    token = await auth_manager.login_otp(schema)

    if token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    response.set_cookie(jwt_security.config.JWT_ACCESS_COOKIE_NAME, token)

    return {"status": "success", "token": token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(jwt_security.config.JWT_ACCESS_COOKIE_NAME)


@router.get("/current")
async def get_current_user(users_service: Annotated[UsersService, Depends(get_users_service)],
                           payload: TokenPayload = Depends(jwt_security.access_token_required)):
    user = await users_service.get_user(int(payload.sub))

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user
