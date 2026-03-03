import datetime
from typing import List

from pydantic import BaseModel

from app.db.enums import OTPTarget
from app.db.enums.mfa_method import MFAMethod
from app.schemas.base_schemas import BaseResponseSchema, BaseRequestWithAccessTokenSchema


class AuthResponseWithAccessTokenSchema(BaseResponseSchema):
    access_token: str
    token_type: str = "bearer"


class AuthLoginRequestSchema(BaseModel):
    username: str
    password: str


class AuthLoginResponseSchema(AuthResponseWithAccessTokenSchema):
    require_mfa_setup: bool = False
    require_mfa_verify: bool = False


class AuthMfaOtpVerifyRequestSchema(BaseRequestWithAccessTokenSchema):
    code: str


class AuthMfaOtpVerifyResponseSchema(AuthResponseWithAccessTokenSchema):
    pass


class AuthMfaOtpSendRequestSchema(BaseRequestWithAccessTokenSchema):
    pass


class AuthMfaOtpSendResponseSchema(BaseResponseSchema):
    code_exp_time: datetime.datetime
    code_send_target_type: OTPTarget
    code_send_to: str


class AuthGetCurrentUserMfaMethodResponseSchema(BaseResponseSchema):
    mfa_method: MFAMethod
