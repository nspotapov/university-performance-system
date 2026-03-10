from typing import Optional
from pydantic import BaseModel


class FacultyBase(BaseModel):
    name: str
    short_name: str
    description: Optional[str] = None


class FacultyCreateRequestSchema(FacultyBase):
    pass


class FacultyUpdateRequestSchema(FacultyBase):
    __annotations__ = {k: Optional[v] for k, v in FacultyBase.__annotations__.items()}


class FacultyReadResponseSchema(FacultyBase):
    id: int

    class Config:
        from_attributes = True
