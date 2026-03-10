from typing import Optional
from datetime import date
from pydantic import BaseModel
from app.models import GradeValue

class GradeBase(BaseModel):
    gradebook_id: int
    student_id: int
    grade_value: GradeValue
    grade_date: date
    comment: Optional[str] = None

class GradeCreateRequestSchema(GradeBase): pass
class GradeUpdateRequestSchema(GradeBase):
    __annotations__ = {k: Optional[v] for k, v in GradeBase.__annotations__.items()}
class GradeReadResponseSchema(GradeBase):
    id: int
    class Config: from_attributes = True
