from pydantic import BaseModel


class OTPReadSchema(BaseModel):
    id: str
    user_id: str
    code: str


class OTPCreateSchema(BaseModel):
    user_id: str
    code: str
