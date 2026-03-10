from typing import Optional
from datetime import date
from pydantic import BaseModel

class CreditBase(BaseModel):
    student_id: int
    discipline_id: int
    semester_id: int
    teacher_id: int
    is_passed: bool
    credit_date: date
    attempt_number: int = 1
    comment: Optional[str] = None

class CreditCreateRequestSchema(CreditBase): pass
class CreditUpdateRequestSchema(CreditBase):
    __annotations__ = {k: Optional[v] for k, v in CreditBase.__annotations__.items()}
class CreditReadResponseSchema(CreditBase):
    id: int
    class Config: from_attributes = True
