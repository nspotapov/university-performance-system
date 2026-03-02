import datetime

from pydantic import BaseModel, EmailStr


class AuthLoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class AuthLoginResponseSchema(BaseModel):
    token: str


class AuthOTPVerifyRequestSchema(BaseModel):
    otp_code: str

class Auth2FAOTPCodeVerifyResponseSchema(BaseModel):
    token: str

class Auth2FAOTPCodeSendResponseSchema(BaseModel):
    otp_code_exp_time: datetime.datetime
    otp_code_send_email: str
