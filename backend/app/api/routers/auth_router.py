import asyncio
import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response

import app.config
from app.api.dependencies import get_auth_service, get_otp_service, get_mail_service, get_user_on_mfa_step
from app.common import text_messages
from app.common.func import mask_email
from app.common.security import jwt_security
from app.db.enums import OTPTarget
from app.db.enums.user_role import UserRole
from app.schemas.auth_schemas import AuthLoginRequestSchema, AuthMfaOtpVerifyRequestSchema, \
    AuthMfaOtpSendResponseSchema, \
    AuthLoginResponseSchema, AuthMfaOtpVerifyResponseSchema, AuthMfaOtpSendRequestSchema, \
    AuthGetCurrentUserMfaMethodResponseSchema
from app.schemas.user_schemas import UserReadSchema
from app.services import AuthService, OTPService, MailService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login")
async def post_login_user(
        schema: AuthLoginRequestSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        response: Response,
) -> AuthLoginResponseSchema:
    user = await auth_service.login_user(schema)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=text_messages.INCORRECT_CREDENTIALS)

    if user.is_mfa_enabled:
        token = jwt_security.create_access_token(
            uid=str(user.id),
            data={app.config.jwt_token_payload_mfa_required_key: True},
            expiry=datetime.timedelta(seconds=app.config.otp_code_expired_time * 2))
    else:
        token = jwt_security.create_access_token(uid=str(user.id))

    resp_schema = AuthLoginResponseSchema(access_token=token)

    if user.is_mfa_enabled:
        resp_schema.require_mfa_verify = True

    if user.role not in [UserRole.STUDENT] and not user.is_mfa_enabled:
        resp_schema.require_mfa_setup = True

    jwt_security.set_access_cookies(token, response)

    return resp_schema


@router.post("/mfa/otp/send")
async def post_send_mfa_otp(
        request_schema: AuthMfaOtpSendRequestSchema,
        otp_service: Annotated[OTPService, Depends(get_otp_service)],
        mail_service: Annotated[MailService, Depends(get_mail_service)],
        current_user: Annotated[UserReadSchema, Depends(get_user_on_mfa_step)],
) -> AuthMfaOtpSendResponseSchema:
    otp = await otp_service.create_otp_code(current_user.id)

    otp_expired_time = datetime.datetime.now() + datetime.timedelta(seconds=app.config.otp_code_expired_time)
    otp_expired_time_str = otp_expired_time.strftime("%H:%M:%S %d.%m.%Y")

    if current_user.mfa_otp_target == OTPTarget.EMAIL:
        msg_text = (text_messages.YOUR_OTP_CODE.format(otp.code) + "\n" +
                    text_messages.OTP_CODE_EXPIRE_TIME.format(otp_expired_time_str))
        msg_subject = text_messages.HEADER_SIGNIN_VERIFY
        asyncio.create_task(mail_service.send_mail(current_user.email, msg_subject, msg_text))
        code_send_to = mask_email(current_user.email)
    else:
        # TODO: Реализовать отправку OTP в другие сервисы кроме Email по необходимости
        raise Exception("Not implemented OTP target")

    resp_schema = AuthMfaOtpSendResponseSchema(
        code_exp_time=otp_expired_time,
        code_send_to=code_send_to,
        code_send_target_type=current_user.mfa_otp_target
    )

    return resp_schema


@router.post("/mfa/otp/verify")
async def post_verify_mfa_otp(
        request_schema: AuthMfaOtpVerifyRequestSchema,
        otp_service: Annotated[OTPService, Depends(get_otp_service)],
        current_user: Annotated[UserReadSchema, Depends(get_user_on_mfa_step)],
        response: Response,
) -> AuthMfaOtpVerifyResponseSchema:
    is_verified = await otp_service.verify_otp_code(
        current_user.id, request_schema.code, delete_code=True
    )

    if not is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=text_messages.INCORRECT_MFA_OTP_CODE)

    token = jwt_security.create_access_token(uid=str(current_user.id))

    jwt_security.set_access_cookies(token, response)

    resp_schema = AuthMfaOtpVerifyResponseSchema(access_token=token)

    return resp_schema


@router.get("/mfa/method")
async def get_current_user_mfa_method(
        current_user: Annotated[UserReadSchema, Depends(get_user_on_mfa_step)],
) -> AuthGetCurrentUserMfaMethodResponseSchema:
    resp_schema = AuthGetCurrentUserMfaMethodResponseSchema(mfa_method=current_user.mfa_method)
    return resp_schema


@router.post("/logout")
async def logout_user(response: Response):
    jwt_security.unset_cookies(response)
