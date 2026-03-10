from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

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
    __annotations__ = {k: Optional[v] for k, v in UserBase.__annotations__.items()}
    password: Optional[str] = None


class UserReadResponseSchema(UserBase):
    id: int
    
    class Config:
        from_attributes = True
        # Исключаем чувствительные поля
        extra = 'ignore'
