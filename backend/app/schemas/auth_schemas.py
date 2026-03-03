import datetime

from pydantic import BaseModel

from app.schemas.base_schemas import BaseResponseSchema, BaseRequestWithAccessTokenSchema


class AuthLoginRequestSchema(BaseModel):
    username: str
    password: str


class AuthLoginResponseSchema(BaseResponseSchema):
    access_token: str
    token_type: str


class AuthOTPVerifyRequestSchema(BaseRequestWithAccessTokenSchema):
    otp_code: str


class Auth2FAOTPCodeSendRequestSchema(BaseRequestWithAccessTokenSchema):
    pass


class Auth2FAOTPCodeVerifyResponseSchema(BaseResponseSchema):
    access_token: str
    token_type: str


class Auth2FAOTPCodeSendResponseSchema(BaseResponseSchema):
    otp_code_exp_time: datetime.datetime
    otp_code_send_email: str
