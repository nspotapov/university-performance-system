import datetime
from typing import Annotated

from authx import TokenPayload
from fastapi import APIRouter, Response, Depends, HTTPException, status

from app.api.dependencies import get_auth_service, get_user_service
from app.core import messages
from app.core.config import settings
from app.core.security import jwt_security, mfa_jwt_security
from app.models import User
from app.services import AuthService, UserService
from .schemas import (
    ApiV1LoginUserRequestSchema,
    ApiV1LoginUserResponseSchema,
    ApiV1VerifyMfaTotpCodeResponseSchema,
    ApiV1VerifyMfaTotpCodeRequestSchema,
    ApiV1GetCurrentUserMfaMethodResponseSchema,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


async def get_user_with_mfa_access_token(
        access_token_payload: Annotated[TokenPayload, Depends(mfa_jwt_security.access_token_required)],
        user_service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    return await user_service.get_user_by_id(int(access_token_payload.sub))


@router.post(
    "/logout",
    responses={
        200: {
            "description": "User logout successful"
        }
    }
)
async def logout_user(response: Response):
    jwt_security.unset_refresh_cookies(response)


@router.post(
    "/login",
    responses={
        200: {
            "description": "Credentials valid and MFA disabled",
            "model": ApiV1LoginUserResponseSchema
        },
        202: {
            "description": "Credentials valid and MFA required",
            "model": ApiV1LoginUserResponseSchema
        },
        400: {
            "description": "Credentials valid but user inactive",
        },
        401: {
            "description": "Invalid credentials",
        },
    }
)
async def login_user(
        request_schema: ApiV1LoginUserRequestSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        response: Response
) -> ApiV1LoginUserResponseSchema:
    user = await auth_service.login_user(request_schema.username, request_schema.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.ERROR_INVALID_CREDENTIALS)
    is_active = await auth_service.check_user_is_active(user)
    if not is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.ERROR_USER_INACTIVE)
    is_mfa_enabled = await auth_service.check_mfa_enabled(user)
    if is_mfa_enabled:
        access_token = mfa_jwt_security.create_access_token(
            uid=str(user.id),
            expiry=datetime.timedelta(minutes=settings.MFA_JWT_EXPIRE_MINUTES)
        )
        response.status_code = 202
    else:
        access_token = jwt_security.create_access_token(uid=str(user.id))
        refresh_token = jwt_security.create_refresh_token(uid=str(user.id))
        jwt_security.set_refresh_cookies(refresh_token, response)
    response_schema = ApiV1LoginUserResponseSchema(access_token=access_token, mfa_required=user.is_mfa_enabled)
    return response_schema


@router.get(
    "/mfa/method",
    responses={
        200: {
            "description": "MFA enabled",
            "model": ApiV1GetCurrentUserMfaMethodResponseSchema
        },
        400: {
            "description": "MFA disabled for this user"
        }
    }
)
async def get_user_mfa_method(
        current_user: Annotated[User, Depends(get_user_with_mfa_access_token)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> ApiV1GetCurrentUserMfaMethodResponseSchema:
    is_mfa_enabled = await auth_service.check_mfa_enabled(current_user)
    if not is_mfa_enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.ERROR_MFA_DISABLED_FOR_THIS_USER)
    user_mfa_method = await auth_service.get_user_mfa_method(current_user)
    response_schema = ApiV1GetCurrentUserMfaMethodResponseSchema(mfa_method=user_mfa_method)
    return response_schema


@router.post(
    "/mfa/totp/verify",
    responses={
        200: {
            "description": "TOTP code valid",
            "model": ApiV1VerifyMfaTotpCodeResponseSchema
        },
        400: {
            "description": "TOTP disabled for this user",
        },
        401: {
            "description": "TOTP code invalid"
        }
    }
)
async def verify_mfa_totp_code(
        request_schema: ApiV1VerifyMfaTotpCodeRequestSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        current_user: Annotated[User, Depends(get_user_with_mfa_access_token)],
        response: Response
) -> ApiV1VerifyMfaTotpCodeResponseSchema:
    is_totp_enabled = await auth_service.check_totp_enabled(current_user)
    if not is_totp_enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.ERROR_TOTP_DISABLED_FOR_THIS_USER)
    is_totp_code_verified = await auth_service.verify_totp_code(current_user, request_schema.code)
    if not is_totp_code_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.ERROR_INVALID_TOTP_CODE)
    access_token = jwt_security.create_access_token(uid=str(current_user.id))
    refresh_token = jwt_security.create_refresh_token(uid=str(current_user.id))
    jwt_security.set_refresh_cookies(refresh_token, response)
    response_schema = ApiV1VerifyMfaTotpCodeResponseSchema(access_token=access_token)
    return response_schema
