from typing import Optional
from datetime import date
from pydantic import BaseModel
from app.models import GradeType

class GradeBookBase(BaseModel):
    semester_id: int
    study_group_id: int
    discipline_id: int
    teacher_id: int
    grade_type: GradeType
    name: str
    created_at: date
    is_closed: bool = False

class GradeBookCreateRequestSchema(GradeBookBase): pass
class GradeBookUpdateRequestSchema(GradeBookBase):
    __annotations__ = {k: Optional[v] for k, v in GradeBookBase.__annotations__.items()}
class GradeBookReadResponseSchema(GradeBookBase):
    id: int
    class Config: from_attributes = True
