from typing import Optional
from pydantic import BaseModel


class StudyDirectionBase(BaseModel):
    faculty_id: int
    name: str
    code: str
    level: str
    description: Optional[str] = None


class StudyDirectionCreateRequestSchema(StudyDirectionBase):
    pass


class StudyDirectionUpdateRequestSchema(StudyDirectionBase):
    __annotations__ = {k: Optional[v] for k, v in StudyDirectionBase.__annotations__.items()}


class StudyDirectionReadResponseSchema(StudyDirectionBase):
    id: int

    class Config:
        from_attributes = True
