from pydantic import BaseModel, EmailStr


class AuthLoginSchema(BaseModel):
    email: EmailStr
    password: str


class AuthOTPLoginSchema(AuthLoginSchema):
    otp_code: str
