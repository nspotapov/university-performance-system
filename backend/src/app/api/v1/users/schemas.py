import uuid

from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class ApiV1ReadUserResponseSchema(BaseModel):
    id: uuid.UUID
    email: EmailStr
    role: UserRole
    is_active: bool


class ApiV1CreateUserResponseSchema(BaseModel):
    email: EmailStr
    role: UserRole
    is_active: bool


class ApiV1ReadUsersResponseSchema(BaseModel):
    pass
