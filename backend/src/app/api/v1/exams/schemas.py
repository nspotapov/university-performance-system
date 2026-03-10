from typing import Optional
from datetime import date
from pydantic import BaseModel
from app.models import GradeValue

class ExamBase(BaseModel):
    student_id: int
    discipline_id: int
    semester_id: int
    teacher_id: int
    grade_value: GradeValue
    exam_date: date
    attempt_number: int = 1
    comment: Optional[str] = None

class ExamCreateRequestSchema(ExamBase): pass
class ExamUpdateRequestSchema(ExamBase):
    __annotations__ = {k: Optional[v] for k, v in ExamBase.__annotations__.items()}
class ExamReadResponseSchema(ExamBase):
    id: int
    class Config: from_attributes = True
