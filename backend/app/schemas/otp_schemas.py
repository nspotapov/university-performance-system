from pydantic import BaseModel


class OTPReadSchema(BaseModel):
    id: str
    user_id: int
    code: str


class OTPCreateSchema(BaseModel):
    user_id: int
    code: str
