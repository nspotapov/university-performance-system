import datetime
from typing import Annotated

from fastapi import APIRouter, Response, Depends, HTTPException, status, Request

from app.api.v1.dependencies import get_auth_service, get_user_service, get_current_user
from app.core import messages
from app.core.config import settings
from app.core.security import jwt_security, mfa_jwt_security
from app.services import AuthService, UserService
from .schemas import (
    ApiV1LoginUserRequestSchema,
    ApiV1LoginUserResponseSchema,
    ApiV1VerifyMfaTotpCodeResponseSchema,
    ApiV1VerifyMfaTotpCodeRequestSchema,
    ApiV1GetCurrentUserMfaMethodResponseSchema, AccessTokenResponse,
)
from ..users.schemas import UserReadResponseSchema

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


async def get_current_user_with_mfa_access_token(
        request: Request,
        user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadResponseSchema:
    # Get access token from HEADERS only (not cookies)
    access_token = await mfa_jwt_security.get_access_token_from_request(
        request,
        locations=["headers"],  # Only look in headers
    )
    # Verify the access token
    # No CSRF verification needed for header-based tokens
    access_token_payload = mfa_jwt_security.verify_token(access_token, verify_csrf=False)
    return await user_service.get_user(int(access_token_payload.sub))


@router.post("/logout")
async def logout_user(response: Response):
    jwt_security.unset_refresh_cookies(response)


@router.post("/login")
async def login_user(
        request_schema: ApiV1LoginUserRequestSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        response: Response
) -> ApiV1LoginUserResponseSchema:
    user = await auth_service.login_user(request_schema.username, request_schema.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.ERROR_INVALID_CREDENTIALS)
    is_active = await auth_service.check_user_is_active(user)
    if not is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.ERROR_USER_INACTIVE)
    is_mfa_enabled = await auth_service.check_mfa_enabled(user)
    if is_mfa_enabled:
        access_token = mfa_jwt_security.create_access_token(
            uid=str(user.id),
            expiry=datetime.timedelta(minutes=settings.MFA_JWT_EXPIRE_MINUTES)
        )
    else:
        access_token = jwt_security.create_access_token(uid=str(user.id))
        refresh_token = jwt_security.create_refresh_token(uid=str(user.id))
        jwt_security.set_refresh_cookies(refresh_token, response)
    response_schema = ApiV1LoginUserResponseSchema(access_token=access_token, mfa_required=user.is_mfa_enabled)
    return response_schema


@router.post("/refresh")
async def refresh_jwt_access_token(request: Request) -> AccessTokenResponse:
    # Get refresh token from COOKIES only (not headers)
    # The locations parameter restricts where to look for the token
    refresh_token = await jwt_security.get_refresh_token_from_request(
        request,
        locations=["cookies"],  # Only look in cookies
    )

    # Verify the refresh token (CSRF is verified automatically for cookies)
    payload = jwt_security.verify_token(refresh_token, verify_type=True)

    # Create a new access token
    new_access_token = jwt_security.create_access_token(uid=payload.sub)

    # Return in response body (client stores in memory)
    return AccessTokenResponse(access_token=new_access_token)


@router.get("/mfa/method")
async def get_user_mfa_method(
        current_user: Annotated[UserReadResponseSchema, Depends(get_current_user_with_mfa_access_token)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> ApiV1GetCurrentUserMfaMethodResponseSchema:
    is_mfa_enabled = await auth_service.check_mfa_enabled(current_user)
    if not is_mfa_enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.ERROR_MFA_DISABLED_FOR_THIS_USER)
    user_mfa_method = await auth_service.get_user_mfa_method(current_user)
    response_schema = ApiV1GetCurrentUserMfaMethodResponseSchema(mfa_method=user_mfa_method)
    return response_schema


@router.post("/mfa/totp/verify")
async def verify_mfa_totp_code(
        request_schema: ApiV1VerifyMfaTotpCodeRequestSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        current_user: Annotated[UserReadResponseSchema, Depends(get_current_user_with_mfa_access_token)],
        response: Response
) -> ApiV1VerifyMfaTotpCodeResponseSchema:
    is_totp_enabled = await auth_service.check_totp_enabled(current_user)
    if not is_totp_enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.ERROR_TOTP_DISABLED_FOR_THIS_USER)
    is_totp_code_verified = await auth_service.verify_totp_code(current_user, request_schema.code)
    if not is_totp_code_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.ERROR_INVALID_TOTP_CODE)
    access_token = jwt_security.create_access_token(uid=str(current_user.id))
    refresh_token = jwt_security.create_refresh_token(uid=str(current_user.id))
    jwt_security.set_refresh_cookies(refresh_token, response)
    response_schema = ApiV1VerifyMfaTotpCodeResponseSchema(access_token=access_token)
    return response_schema


@router.get("/current-user")
async def get_current_user(
        current_user: Annotated[UserReadResponseSchema, Depends(get_current_user)],
) -> UserReadResponseSchema:
    return current_user
