from typing import Optional

from pydantic import Field, EmailStr

from .base_schemas import BaseCreateSchema, BaseReadSchema, BaseUpdateSchema
from ..db.enums import UserRole, OTPTarget, MFAMethod


class UserCreateSchema(BaseCreateSchema):
    name: str = Field(max_length=64)
    email: EmailStr
    password: str = Field(max_length=64)
    role: UserRole = Field(default=UserRole.STUDENT)
    is_active: bool = Field(default=True)
    is_mfa_enabled: bool = Field(default=False)
    mfa_method: MFAMethod = Field(default=MFAMethod.OTP)
    mfa_otp_target: OTPTarget


class UserReadSchema(BaseReadSchema):
    name: str
    email: str
    hashed_password: str = Field(exclude=True)
    role: UserRole
    is_active: bool
    totp_secret: Optional[str] = Field(exclude=True)
    is_mfa_enabled: bool
    mfa_method: MFAMethod
    mfa_otp_target: OTPTarget


class UserUpdateSchema(BaseUpdateSchema):
    name: None | str = Field(max_length=64)
    email: None | EmailStr
    password: None | str = Field(max_length=64)
    role: UserRole
    is_active: bool
    is_mfa_enabled: bool
    mfa_method: MFAMethod
    mfa_otp_target: OTPTarget
