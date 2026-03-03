from typing import Annotated

from authx import TokenPayload
from fastapi import Depends, HTTPException, status

import app.config
from app.common import text_messages
from app.common.security import jwt_security
from app.db.models.user_model import UserRole
from app.repositories import UsersRepository, OTPRepository
from app.schemas.user_schemas import UserReadSchema
from app.services import UsersService, AuthService, OTPService, MailService


def get_users_service():
    return UsersService(UsersRepository)


def get_auth_service():
    return AuthService(UsersRepository)


def get_otp_service():
    return OTPService(OTPRepository)


def get_mail_service():
    return MailService()


async def get_user_on_mfa_step(
        users_service: Annotated[UsersService, Depends(get_users_service)],
        access_token_payload: TokenPayload = Depends(jwt_security.access_token_required),
) -> UserReadSchema:
    required_mfa = access_token_payload.model_extra.get(app.config.jwt_token_payload_mfa_required_key)

    if not required_mfa:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=text_messages.MULTI_FACTOR_FACTOR_AUTH_NOT_REQUIRED)

    user = await users_service.get_user(access_token_payload.sub)

    return user


async def get_authorized_user(
        users_service: Annotated[UsersService, Depends(get_users_service)],
        access_token_payload: TokenPayload = Depends(jwt_security.access_token_required),
) -> UserReadSchema:
    required_mfa = access_token_payload.model_extra.get(app.config.jwt_token_payload_mfa_required_key)

    if required_mfa is not None and required_mfa:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=text_messages.MULTI_FACTOR_AUTH_REQUIRED)

    current_user = await users_service.get_user(access_token_payload.sub)

    return current_user


def check_role(roles: list[UserRole]):
    def role_checker(current_user: UserReadSchema = Depends(get_authorized_user)) -> UserReadSchema:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"The user doesn't have enough privileges. Required: {",".join([x.value for x in roles])}"
            )
        return current_user

    return role_checker
