from typing import Optional

from sqlalchemy import String, Enum, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from app.schemas.user_schemas import UserReadSchema
from .base_model import BaseDbModelWithId
from ..enums import UserRole, MFAMethod, OTPTarget


class User(BaseDbModelWithId):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.STUDENT)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    totp_secret: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    mfa_method: Mapped[MFAMethod] = mapped_column(Enum(MFAMethod), default=MFAMethod.OTP)
    mfa_otp_target: Mapped[OTPTarget] = mapped_column(Enum(OTPTarget), default=OTPTarget.EMAIL)

    def to_read_schema(self) -> UserReadSchema:
        return UserReadSchema(
            id=self.id,
            name=self.name,
            email=self.email,
            hashed_password=self.hashed_password,
            role=self.role,
            is_active=self.is_active,
            totp_secret=self.totp_secret,
            is_mfa_enabled=self.is_mfa_enabled,
            mfa_method=self.mfa_method,
            mfa_otp_target=self.mfa_otp_target
        )
