from typing import Optional
from pydantic import BaseModel


class FacultyBase(BaseModel):
    name: str
    short_name: str
    description: Optional[str] = None

class FacultyCreateRequestSchema(FacultyBase): pass
class FacultyUpdateRequestSchema(FacultyBase):
    __annotations__ = {k: Optional[v] for k, v in FacultyBase.__annotations__.items()}
class FacultyReadResponseSchema(FacultyBase):
    id: int
    class Config: from_attributes = True

class DepartmentBase(BaseModel):
    faculty_id: int
    name: str
    short_name: str
    description: Optional[str] = None

class DepartmentCreateRequestSchema(DepartmentBase): pass
class DepartmentUpdateRequestSchema(DepartmentBase):
    __annotations__ = {k: Optional[v] for k, v in DepartmentBase.__annotations__.items()}
class DepartmentReadResponseSchema(DepartmentBase):
    id: int
    class Config: from_attributes = True

class StudyDirectionBase(BaseModel):
    faculty_id: int
    name: str
    code: str
    level: str
    description: Optional[str] = None

class StudyDirectionCreateRequestSchema(StudyDirectionBase): pass
class StudyDirectionUpdateRequestSchema(StudyDirectionBase):
    __annotations__ = {k: Optional[v] for k, v in StudyDirectionBase.__annotations__.items()}
class StudyDirectionReadResponseSchema(StudyDirectionBase):
    id: int
    class Config: from_attributes = True

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

class CourseBase(BaseModel):
    number: int
    description: Optional[str] = None

class CourseCreateRequestSchema(CourseBase): pass
class CourseUpdateRequestSchema(CourseBase):
    __annotations__ = {k: Optional[v] for k, v in CourseBase.__annotations__.items()}
class CourseReadResponseSchema(CourseBase):
    id: int
    class Config: from_attributes = True

class SemesterBase(BaseModel):
    course_id: int
    number: int
    name: str
    start_date: str
    end_date: str
    is_active: bool = False

class SemesterCreateRequestSchema(SemesterBase): pass
class SemesterUpdateRequestSchema(SemesterBase):
    __annotations__ = {k: Optional[v] for k, v in SemesterBase.__annotations__.items()}
class SemesterReadResponseSchema(SemesterBase):
    id: int
    class Config: from_attributes = True

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
