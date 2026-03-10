from typing import Optional
from pydantic import BaseModel
class CurriculumBase(BaseModel):
    study_direction_id: int
    name: str
    year: int
    description: Optional[str] = None
class CurriculumCreateRequestSchema(CurriculumBase): pass
class CurriculumUpdateRequestSchema(CurriculumBase):
    __annotations__ = {k: Optional[v] for k, v in CurriculumBase.__annotations__.items()}
class CurriculumReadResponseSchema(CurriculumBase):
    id: int
    class Config: from_attributes = True
