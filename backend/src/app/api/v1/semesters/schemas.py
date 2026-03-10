from typing import Optional
from pydantic import BaseModel
class SemesterBase(BaseModel):
    course_id: int
    number: int
    name: str
    start_date: str
    end_date: str
    is_active: bool = False
class SemesterCreateRequestSchema(SemesterBase): pass
class SemesterUpdateRequestSchema(SemesterBase):
    __annotations__ = {k: Optional[v] for k, v in SemesterBase.__annotations__.items()}
class SemesterReadResponseSchema(SemesterBase):
    id: int
    class Config: from_attributes = True
