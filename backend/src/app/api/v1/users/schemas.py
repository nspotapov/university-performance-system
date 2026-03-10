from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models import MFAMethod
from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole
    is_active: bool = True
    is_mfa_enabled: bool = False
    mfa_method: MFAMethod


class UserCreateRequestSchema(UserBase):
    password: str


class UserUpdateRequestSchema(UserBase):
    # Делаем все поля базовой схемы опциональными для PATCH/PUT
    __annotations__ = {k: Optional[v] for k, v in UserBase.__annotations__.items()}
    password: Optional[str] = None


class UserReadResponseSchema(UserBase):
    id: int
    # hashed_password и totp_secret исключаем через Field(exclude=True)
    # или просто не объявляем их здесь
    class Config:
        from_attributes = True
