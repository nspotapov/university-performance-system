from typing import Optional
from pydantic import BaseModel, Field, EmailStr

from app.models import MFAMethod


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 900  # 15 minutes in seconds


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 900


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    mfa_required: bool
    mfa_method: Optional[MFAMethod] = None
    message: Optional[str] = None  # Сообщение если требуется настройка 2FA


class VerifyTotpRequestSchema(BaseModel):
    code: str = Field(min_length=6, max_length=6, description="6-значный код из Google Authenticator")


class VerifyTotpResponseSchema(AccessTokenResponse):
    pass


class VerifyOtpRequestSchema(BaseModel):
    code: str = Field(min_length=6, max_length=6, description="6-значный OTP код из email")


class VerifyOtpResponseSchema(AccessTokenResponse):
    pass


class SendOtpResponseSchema(BaseModel):
    message: str = "OTP код отправлен на вашу почту"
    expires_in: int = 600  # 10 minutes


class TotpSetupResponseSchema(BaseModel):
    secret: str
    qr_code_uri: str
    message: str = "Отсканируйте QR код в Google Authenticator и подтвердите код"


class MfaMethodResponseSchema(BaseModel):
    is_enabled: bool
    method: Optional[MFAMethod] = None
    is_required: bool  # Обязательна ли 2FA для этой роли


class EnableMfaRequestSchema(BaseModel):
    method: MFAMethod
    password: Optional[str] = None  # Требуется для включения OTP


class DisableMfaRequestSchema(BaseModel):
    password: str  # Требуется подтверждение паролем
