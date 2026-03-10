from typing import Annotated, Optional
from datetime import datetime

from fastapi import APIRouter, Response, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.dependencies import get_auth_service, get_user_service, get_current_user
from app.core import messages
from app.core.security import jwt_security, mfa_jwt_security
from app.models import UserRole, MFAMethod
from app.services import AuthService, UserService
from .schemas import (
    LoginRequestSchema,
    LoginResponseSchema,
    VerifyTotpRequestSchema,
    VerifyTotpResponseSchema,
    VerifyOtpRequestSchema,
    VerifyOtpResponseSchema,
    SendOtpResponseSchema,
    TotpSetupResponseSchema,
    MfaMethodResponseSchema,
    EnableMfaRequestSchema,
    DisableMfaRequestSchema,
    AccessTokenResponse,
    RefreshTokenResponse,
)
from ..users.schemas import UserReadResponseSchema

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ============================================================================
# Helper для получения пользователя с MFA токеном
# ============================================================================

async def get_current_user_with_mfa_token(
    request: Request,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadResponseSchema:
    """
    Получение текущего пользователя с MFA токеном.
    MFA токен принимается только из заголовка Authorization.
    """
    access_token = await mfa_jwt_security.get_access_token_from_request(
        request,
        locations=["headers"],
    )
    access_token_payload = mfa_jwt_security.verify_token(access_token, verify_csrf=False)
    return await user_service.get_user(int(access_token_payload.sub))


# ============================================================================
# OAuth2 Token Endpoint
# ============================================================================

@router.post("/token")
async def oauth2_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    response: Response
) -> LoginResponseSchema:
    """OAuth2 совместимый endpoint для входа."""
    return await login_user(LoginRequestSchema(email=form_data.username, password=form_data.password), auth_service, response)


# ============================================================================
# Login / Logout
# ============================================================================

@router.post("/login")
async def login_user(
    request_schema: LoginRequestSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    response: Response
) -> LoginResponseSchema:
    user = await auth_service.login_user(request_schema.email, request_schema.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.ERROR_INVALID_CREDENTIALS)
    
    is_active = await auth_service.check_user_is_active(user)
    if not is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=messages.ERROR_USER_INACTIVE)
    
    if auth_service.should_require_mfa_on_login(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=messages.ERROR_MFA_REQUIRED,
            headers={"X-MFA-Required": "true"}
        )
    
    is_mfa_enabled = await auth_service.check_mfa_enabled(user)
    
    if is_mfa_enabled:
        mfa_token = mfa_jwt_security.create_access_token(uid=str(user.id))
        return LoginResponseSchema(
            access_token=mfa_token,
            token_type="bearer",
            mfa_required=True,
            mfa_method=user.mfa_method,
            message="Требуется подтверждение второго фактора"
        )
    else:
        access_token = jwt_security.create_access_token(uid=str(user.id))
        refresh_token = jwt_security.create_refresh_token(uid=str(user.id))
        jwt_security.set_refresh_cookies(refresh_token, response)
        
        return LoginResponseSchema(
            access_token=access_token,
            token_type="bearer",
            mfa_required=False,
            mfa_method=None,
            message=None
        )


@router.post("/logout")
async def logout_user(response: Response):
    jwt_security.unset_refresh_cookies(response)
    return {"message": "Успешный выход"}


# ============================================================================
# Token Refresh
# ============================================================================

@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_access_token(
    request: Request,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RefreshTokenResponse:
    refresh_token = await jwt_security.get_refresh_token_from_request(
        request,
        locations=["cookies"],
    )
    
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.ERROR_REFRESH_TOKEN_NOT_FOUND,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt_security.verify_token(refresh_token, verify_type=True)
        user_id = int(payload.sub)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.ERROR_INVALID_TOKEN,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await auth_service.get_user_with_refresh(user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.ERROR_USER_INACTIVE,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    new_access_token = jwt_security.create_access_token(uid=str(user.id))
    
    return RefreshTokenResponse(
        access_token=new_access_token,
        token_type="bearer",
        expires_in=int(jwt_security.access_token_expires.total_seconds())
    )


# ============================================================================
# MFA - TOTP (Google Authenticator)
# ============================================================================

@router.post("/mfa/totp/verify", response_model=VerifyTotpResponseSchema)
async def verify_totp_code(
    request_schema: VerifyTotpRequestSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    current_user: Annotated[UserReadResponseSchema, Depends(get_current_user_with_mfa_token)],
    response: Response
) -> VerifyTotpResponseSchema:
    is_totp_enabled = await auth_service.check_totp_enabled(current_user)
    if not is_totp_enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.ERROR_TOTP_DISABLED_FOR_THIS_USER)
    
    is_verified = await auth_service.verify_totp_code(current_user, request_schema.code)
    if not is_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.ERROR_INVALID_TOTP_CODE)
    
    access_token = jwt_security.create_access_token(uid=str(current_user.id))
    refresh_token = jwt_security.create_refresh_token(uid=str(current_user.id))
    jwt_security.set_refresh_cookies(refresh_token, response)
    
    return VerifyTotpResponseSchema(
        access_token=access_token,
        token_type="bearer",
        expires_in=int(jwt_security.access_token_expires.total_seconds())
    )


# ============================================================================
# MFA - OTP (Email)
# ============================================================================

@router.post("/mfa/otp/send", response_model=SendOtpResponseSchema)
async def send_otp_code(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    current_user: Annotated[UserReadResponseSchema, Depends(get_current_user_with_mfa_token)],
) -> SendOtpResponseSchema:
    await auth_service.send_otp_code(current_user)
    from app.core.config import settings
    return SendOtpResponseSchema(
        message="OTP код отправлен на вашу почту",
        expires_in=settings.OTP_CODE_EXPIRE_MINUTES * 60
    )


@router.post("/mfa/otp/verify", response_model=VerifyOtpResponseSchema)
async def verify_otp_code(
    request_schema: VerifyOtpRequestSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    current_user: Annotated[UserReadResponseSchema, Depends(get_current_user_with_mfa_token)],
    response: Response
) -> VerifyOtpResponseSchema:
    if current_user.mfa_method != MFAMethod.OTP:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP аутентификация не включена")
    
    is_verified = await auth_service.verify_otp_code(current_user, request_schema.code)
    if not is_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.ERROR_INVALID_OTP_CODE)
    
    access_token = jwt_security.create_access_token(uid=str(current_user.id))
    refresh_token = jwt_security.create_refresh_token(uid=str(current_user.id))
    jwt_security.set_refresh_cookies(refresh_token, response)
    
    return VerifyOtpResponseSchema(
        access_token=access_token,
        token_type="bearer",
        expires_in=int(jwt_security.access_token_expires.total_seconds())
    )


# ============================================================================
# MFA Setup & Management
# ============================================================================

@router.get("/mfa/status", response_model=MfaMethodResponseSchema)
async def get_mfa_status(
    current_user: Annotated[UserReadResponseSchema, Depends(get_current_user)],
) -> MfaMethodResponseSchema:
    return MfaMethodResponseSchema(
        is_enabled=current_user.is_mfa_enabled,
        method=current_user.mfa_method if current_user.is_mfa_enabled else None,
        is_required=UserRole.is_mfa_required(current_user.role)
    )


@router.post("/mfa/totp/setup", response_model=TotpSetupResponseSchema)
async def setup_totp(
    current_user: Annotated[UserReadResponseSchema, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> TotpSetupResponseSchema:
    secret, qr_code_uri = await auth_service.setup_totp(current_user)
    return TotpSetupResponseSchema(
        secret=secret,
        qr_code_uri=qr_code_uri,
        message="Отсканируйте QR код в Google Authenticator"
    )


@router.post("/mfa/totp/enable")
async def enable_totp(
    request_schema: VerifyTotpRequestSchema,
    current_user: Annotated[UserReadResponseSchema, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict:
    success = await auth_service.enable_totp(current_user, request_schema.code)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.ERROR_INVALID_TOTP_CODE)
    return {"message": "TOTP аутентификация успешно включена"}


@router.post("/mfa/otp/enable")
async def enable_otp(
    current_user: Annotated[UserReadResponseSchema, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict:
    await auth_service.enable_otp(current_user)
    return {"message": "OTP аутентификация успешно включена"}


@router.post("/mfa/disable")
async def disable_mfa(
    request_schema: DisableMfaRequestSchema,
    current_user: Annotated[UserReadResponseSchema, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict:
    if UserRole.is_mfa_required(current_user.role):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Отключение 2FA недоступно для вашей роли")
    
    success = await auth_service.disable_mfa(current_user, request_schema.password)
    if not success:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.ERROR_INVALID_CREDENTIALS)
    return {"message": "MFA аутентификация успешно отключена"}


# ============================================================================
# Current User
# ============================================================================

@router.get("/me", response_model=UserReadResponseSchema)
async def get_current_user_info(
    current_user: Annotated[UserReadResponseSchema, Depends(get_current_user)],
) -> UserReadResponseSchema:
    return current_user
