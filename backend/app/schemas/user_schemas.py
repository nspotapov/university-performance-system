from pydantic import Field, EmailStr

from app.schemas import BaseSchema


class UserCreateSchema(BaseSchema):
    name: str = Field(description="Имя")
    surname: str = Field(description="Фамилия")
    patronymic: str | None = Field(description="Отчество", default=None)
    email: EmailStr = Field(description="Адрес электронной почты")
    password: str = Field(description="Пароль")


class UserUpdateSchema(BaseSchema):
    name: str | None = Field(description="Имя", default=None)
    surname: str | None = Field(description="Фамилия", default=None)
    patronymic: str | None = Field(description="Отчество", default=None)
    email: EmailStr | None = Field(description="Адрес электронной почты", default=None)
    password: str | None = Field(description="Пароль", default=None)


class UserSchema(BaseSchema):
    id: int
    name: str = Field(description="Имя")
    surname: str = Field(description="Фамилия")
    patronymic: str | None = Field(description="Отчество", default=None)
    email: EmailStr = Field(description="Адрес электронной почты")
