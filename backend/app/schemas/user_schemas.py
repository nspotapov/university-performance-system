from pydantic import Field, EmailStr

from .base_schemas import BaseCreateSchema, BaseReadSchema, BaseUpdateSchema


class UserCreateSchema(BaseCreateSchema):
    name: str = Field(max_length=64)
    email: EmailStr
    password: str = Field(max_length=64)


class UserReadSchema(BaseReadSchema):
    name: str
    email: str
    hashed_password: str = Field(exclude=True)


class UserUpdateSchema(BaseUpdateSchema):
    name: None | str = Field(max_length=64)
    email: None | EmailStr
    password: None | str = Field(max_length=64)
