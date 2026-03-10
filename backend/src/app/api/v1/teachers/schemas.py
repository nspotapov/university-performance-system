from typing import Optional
from datetime import date
from pydantic import BaseModel

class TeacherBase(BaseModel):
    user_id: int
    department_id: int
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    position: str
    academic_degree: Optional[str] = None
    academic_title: Optional[str] = None
    hire_date: date
    is_fired: bool = False
    description: Optional[str] = None

class TeacherCreateRequestSchema(TeacherBase): pass
class TeacherUpdateRequestSchema(TeacherBase):
    __annotations__ = {k: Optional[v] for k, v in TeacherBase.__annotations__.items()}
class TeacherReadResponseSchema(TeacherBase):
    id: int
    class Config: from_attributes = True
