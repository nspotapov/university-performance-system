from typing import Optional
from pydantic import BaseModel


class DepartmentBase(BaseModel):
    faculty_id: int
    name: str
    short_name: str
    description: Optional[str] = None


class DepartmentCreateRequestSchema(DepartmentBase):
    pass


class DepartmentUpdateRequestSchema(DepartmentBase):
    __annotations__ = {k: Optional[v] for k, v in DepartmentBase.__annotations__.items()}


class DepartmentReadResponseSchema(DepartmentBase):
    id: int

    class Config:
        from_attributes = True
