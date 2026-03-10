from typing import Optional
from pydantic import BaseModel
class CourseBase(BaseModel):
    number: int
    description: Optional[str] = None
class CourseCreateRequestSchema(CourseBase): pass
class CourseUpdateRequestSchema(CourseBase):
    __annotations__ = {k: Optional[v] for k, v in CourseBase.__annotations__.items()}
class CourseReadResponseSchema(CourseBase):
    id: int
    class Config: from_attributes = True
