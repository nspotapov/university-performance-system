import asyncio
import datetime
from typing import Annotated

from authx import TokenPayload
from fastapi import APIRouter, Depends, HTTPException, status, Response

import app.config
from app.api.dependencies import get_users_service, get_auth_service, get_otp_service, get_mail_service, \
    get_authenticated_user
from app.common import text_messages
from app.common.func import mask_email
from app.common.security import jwt_security
from app.schemas.auth_schemas import AuthLoginRequestSchema, AuthOTPVerifyRequestSchema, \
    Auth2FAOTPCodeSendResponseSchema, \
    AuthLoginResponseSchema, Auth2FAOTPCodeVerifyResponseSchema
from app.schemas.user_schemas import UserReadSchema
from app.services import UsersService, AuthService, OTPService, MailService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login")
async def login_user(
        schema: AuthLoginRequestSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        response: Response,
):
    user = await auth_service.login_user(schema)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=text_messages.INCORRECT_EMAIL_OR_PASSWORD)

    token = jwt_security.create_access_token(uid=str(user.id),
                                             data={app.config.jwt_token_payload_2fa_required_key: True},
                                             expiry=datetime.timedelta(seconds=app.config.otp_code_expired_time + 60))

    response.set_cookie(jwt_security.config.JWT_ACCESS_COOKIE_NAME, token)

    resp_schema = AuthLoginResponseSchema(token=token)

    return resp_schema


@router.post("/2fa/otp/send")
async def send_2fa_otp_code(
        users_service: Annotated[UsersService, Depends(get_users_service)],
        otp_service: Annotated[OTPService, Depends(get_otp_service)],
        mail_service: Annotated[MailService, Depends(get_mail_service)],
        access_token_payload: TokenPayload = Depends(jwt_security.access_token_required),
):
    required_2fa = access_token_payload.model_extra.get(app.config.jwt_token_payload_2fa_required_key)

    if not required_2fa:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=text_messages.TWO_FACTOR_AUTH_NOT_REQUIRED)

    user = await users_service.get_user(access_token_payload.sub)

    otp = await otp_service.create_otp_code(user.id)

    otp_expired_time = datetime.datetime.now() + datetime.timedelta(seconds=app.config.otp_code_expired_time)
    otp_expired_time_str = otp_expired_time.strftime("%H:%M:%S %d.%m.%Y")

    msg_text = text_messages.YOUR_OTP_CODE.format(otp.code) + \
               + text_messages.OTP_CODE_EXPIRE_TIME.format(otp_expired_time_str)
    msg_subject = text_messages.HEADER_SIGNIN_VERIFY

    asyncio.create_task(mail_service.send_mail(user.email, msg_subject, msg_text))

    resp_schema = Auth2FAOTPCodeSendResponseSchema(otp_code_exp_time=otp_expired_time,
                                                   otp_code_send_email=mask_email(user.email))

    return resp_schema


@router.post("/2fa/otp/verify")
async def verify_2fa_otp_code(
        schema: AuthOTPVerifyRequestSchema,
        otp_service: Annotated[OTPService, Depends(get_otp_service)],
        users_service: Annotated[UsersService, Depends(get_users_service)],
        response: Response,
        access_token_payload: TokenPayload = Depends(jwt_security.access_token_required),
):
    required_2fa = access_token_payload.model_extra.get(app.config.jwt_token_payload_2fa_required_key)

    if not required_2fa:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=text_messages.TWO_FACTOR_AUTH_NOT_REQUIRED)

    user = await users_service.get_user(access_token_payload.sub)

    is_verified = await otp_service.verify_otp_code(
        user.id, schema.otp_code, delete_code=True
    )

    if not is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=text_messages.INCORRECT_2FA_OTP_CODE)

    token = jwt_security.create_access_token(uid=str(user.id))

    response.set_cookie(jwt_security.config.JWT_ACCESS_COOKIE_NAME, token)

    resp_schema = Auth2FAOTPCodeVerifyResponseSchema(token=token)

    return resp_schema


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(jwt_security.config.JWT_ACCESS_COOKIE_NAME)


@router.get("/current-user")
async def get_current_user(user: Annotated[UserReadSchema, Depends(get_authenticated_user)]) -> UserReadSchema:
    return user
