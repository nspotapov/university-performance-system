from pydantic import BaseModel, EmailStr, Field


class AuthLoginSchema(BaseModel):
    email: EmailStr = Field(examples=["ns.potapov@yandex.ru"])
    password: str


class AuthOTPLoginSchema(AuthLoginSchema):
    otp_code: str
