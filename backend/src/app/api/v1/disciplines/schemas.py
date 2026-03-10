from typing import Optional
from pydantic import BaseModel

class DisciplineBase(BaseModel):
    study_direction_id: int
    department_id: int
    name: str
    code: str
    hours: int
    description: Optional[str] = None

class DisciplineCreateRequestSchema(DisciplineBase): pass
class DisciplineUpdateRequestSchema(DisciplineBase):
    __annotations__ = {k: Optional[v] for k, v in DisciplineBase.__annotations__.items()}
class DisciplineReadResponseSchema(DisciplineBase):
    id: int
    class Config: from_attributes = True
