import datetime
from enum import StrEnum
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class MFAMethod(StrEnum):
    OTP = "OTP"  # Код из email
    TOTP = "TOTP"  # Google Authenticator


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    RECTOR = "RECTOR"
    DEAN = "DEAN"
    HEAD_TEACHER = "HEAD_TEACHER"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"

    @classmethod
    def is_mfa_required(cls, role: "UserRole") -> bool:
        """Проверка обязательности 2FA для роли"""
        return role != cls.STUDENT


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(default=UserRole.STUDENT)
    is_active: Mapped[bool] = mapped_column(default=True)
    
    # MFA settings
    is_mfa_enabled: Mapped[bool] = mapped_column(default=False)
    mfa_method: Mapped[MFAMethod] = mapped_column(default=MFAMethod.OTP)
    totp_secret: Mapped[Optional[str]]  # Секрет для TOTP (Google Authenticator)
    
    # OTP settings (for email verification)
    otp_code: Mapped[Optional[str]]  # Текущий OTP код
    otp_expires_at: Mapped[Optional[datetime.datetime]]  # Время истечения OTP кода
