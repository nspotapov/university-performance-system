import datetime

from app.schemas.otp_schemas import OTPReadSchema


class OTP:
    user_id: str
    code: str
    created_at: datetime.datetime

    def to_read_schema(self) -> OTPReadSchema:
        return OTPReadSchema(user_id=self.user_id, code=self.code)
