from typing import Annotated

from authx import TokenPayload
from fastapi import APIRouter, Depends, HTTPException, status, Response

import app.config
from app.api.dependencies import get_users_service, get_auth_service, get_otp_service, get_mail_service
from app.common.security import jwt_security
from app.schemas.auth_schemas import AuthLoginSchema, AuthOTPLoginSchema
from app.schemas.user_schemas import UserReadSchema
from app.services import UsersService, AuthService, OTPService, MailService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login")
async def login_user(
        schema: AuthLoginSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        otp_service: Annotated[OTPService, Depends(get_otp_service)],
        mail_service: Annotated[MailService, Depends(get_mail_service)],
):
    user = await auth_service.login_user(schema)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Неверный email или пароль")

    otp = await otp_service.create_otp_code(user.id)

    otp_expired_time_str = "{} минут".format(app.config.otp_code_expired_time // 60)

    msg_text = f"Ваш код подтверждения: {otp.code}\n\nКод действителен {otp_expired_time_str}"
    msg_subject = "Подтверждение входа на портале университета"

    await mail_service.send_mail(user.email, msg_subject, msg_text)

    return {"detail": "Код подтверждения выслан на указанную вами почту"}


@router.post("/otp")
async def login_user_otp(
        schema: AuthOTPLoginSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        otp_service: Annotated[OTPService, Depends(get_otp_service)],
        response: Response,
):
    user = await auth_service.login_user(schema)

    if user is None:
        return None

    is_verified = await otp_service.verify_otp_code(
        user.id, schema.otp_code, delete_code=True
    )

    if not is_verified:
        return None

    token = jwt_security.create_access_token(uid=str(user.id))

    if token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    response.set_cookie(jwt_security.config.JWT_ACCESS_COOKIE_NAME, token)

    return {"token": token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(jwt_security.config.JWT_ACCESS_COOKIE_NAME)


@router.get("/current-user")
async def get_current_user(
        users_service: Annotated[UsersService, Depends(get_users_service)],
        access_token_payload: TokenPayload = Depends(jwt_security.access_token_required),
) -> UserReadSchema:
    return await users_service.get_user(int(access_token_payload.sub))
