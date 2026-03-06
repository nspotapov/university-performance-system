from pydantic import BaseModel, Field

from app.models import MFAMethod


class BaseResponseWithAccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ApiV1LoginUserRequestSchema(BaseModel):
    username: str
    password: str


class ApiV1LoginUserResponseSchema(BaseResponseWithAccessToken):
    mfa_required: bool


class ApiV1VerifyMfaTotpCodeRequestSchema(BaseModel):
    code: str = Field(min_length=6, max_length=6)


class ApiV1VerifyMfaTotpCodeResponseSchema(BaseResponseWithAccessToken):
    pass


class ApiV1GetCurrentUserMfaMethodResponseSchema(BaseModel):
    mfa_method: MFAMethod
