import datetime
import uuid
from enum import StrEnum
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class MFAMethod(StrEnum):
    OTP = "OTP"
    TOTP = "TOTP"


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    RECTOR = "RECTOR"
    DEAN = "DEAN"
    HEAD_TEACHER = "HEAD_TEACHER"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(insert_default=uuid.uuid4, primary_key=True, index=True)
    email: Mapped[str]
    hashed_password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(default=UserRole.STUDENT)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(insert_default=datetime.datetime.now)
    is_mfa_enabled: Mapped[bool] = mapped_column(default=False)
    mfa_method: Mapped[MFAMethod] = mapped_column(default=MFAMethod.OTP)
    totp_secret: Mapped[Optional[str]]

