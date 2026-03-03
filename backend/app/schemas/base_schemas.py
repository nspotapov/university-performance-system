from typing import Optional

from pydantic import BaseModel


class BaseSchema(BaseModel):
    pass


class BaseCreateSchema(BaseSchema):
    pass


class BaseReadSchema(BaseSchema):
    id: str

    class Config:
        from_attributes = True


class BaseUpdateSchema(BaseSchema):
    pass


class BaseRequestSchema(BaseModel):
    pass


class BaseResponseSchema(BaseModel):
    pass

class BaseRequestWithAccessTokenSchema(BaseRequestSchema):
    access_token: Optional[str] = None
