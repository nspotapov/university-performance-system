from typing import Optional
from pydantic import BaseModel
class StudyGroupBase(BaseModel):
    study_direction_id: int
    course_id: int
    name: str
    year: int
    description: Optional[str] = None
class StudyGroupCreateRequestSchema(StudyGroupBase): pass
class StudyGroupUpdateRequestSchema(StudyGroupBase):
    __annotations__ = {k: Optional[v] for k, v in StudyGroupBase.__annotations__.items()}
class StudyGroupReadResponseSchema(StudyGroupBase):
    id: int
    class Config: from_attributes = True
