from typing import Optional
from datetime import date
from pydantic import BaseModel

class StudentBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    birth_date: date
    enrollment_year: int
    is_expelled: bool = False
    expulsion_reason: Optional[str] = None
    description: Optional[str] = None

class StudentCreateRequestSchema(StudentBase): pass
class StudentUpdateRequestSchema(StudentBase):
    __annotations__ = {k: Optional[v] for k, v in StudentBase.__annotations__.items()}
class StudentReadResponseSchema(StudentBase):
    id: int
    class Config: from_attributes = True
