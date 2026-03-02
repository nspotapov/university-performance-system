from typing import Annotated

from authx import TokenPayload
from fastapi import Depends, HTTPException, status

import app.config
from app.common import text_messages
from app.common.security import jwt_security
from app.repositories import UsersRepository, OTPRepository
from app.services import UsersService, AuthService, OTPService, MailService


def get_users_service():
    return UsersService(UsersRepository)


def get_auth_service():
    return AuthService(UsersRepository)


def get_otp_service():
    return OTPService(OTPRepository)


def get_mail_service():
    return MailService()


async def get_authenticated_user(
        users_service: Annotated[UsersService, Depends(get_users_service)],
        access_token_payload: TokenPayload = Depends(jwt_security.access_token_required),
):
    required_2fa = access_token_payload.model_extra.get(app.config.jwt_token_payload_2fa_required_key)

    if required_2fa is not None and required_2fa:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=text_messages.TWO_FACTOR_AUTH_REQUIRED)

    user = await users_service.get_user(access_token_payload.sub)

    return user
