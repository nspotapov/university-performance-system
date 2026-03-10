from typing import Optional
from datetime import date
from pydantic import BaseModel, ConfigDict
from app.models import GradeType, GradeValue

class StudentBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    birth_date: date
    enrollment_year: int
    is_expelled: bool = False
    expulsion_reason: Optional[str] = None
    description: Optional[str] = None

class StudentCreateRequestSchema(StudentBase): pass
class StudentUpdateRequestSchema(StudentBase):
    __annotations__ = {k: Optional[v] for k, v in StudentBase.__annotations__.items()}
class StudentReadResponseSchema(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

class StudentGroupBase(BaseModel):
    student_id: int
    study_group_id: int
    start_date: date
    end_date: Optional[date] = None
    is_current: bool = True

class StudentGroupCreateRequestSchema(StudentGroupBase): pass
class StudentGroupUpdateRequestSchema(StudentGroupBase):
    __annotations__ = {k: Optional[v] for k, v in StudentGroupBase.__annotations__.items()}
class StudentGroupReadResponseSchema(StudentGroupBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

class GradeBase(BaseModel):
    gradebook_id: int
    student_id: int
    grade_value: GradeValue
    grade_date: date
    comment: Optional[str] = None

class GradeCreateRequestSchema(GradeBase): pass
class GradeUpdateRequestSchema(GradeBase):
    __annotations__ = {k: Optional[v] for k, v in GradeBase.__annotations__.items()}
class GradeReadResponseSchema(GradeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CreditBase(BaseModel):
    student_id: int
    discipline_id: int
    semester_id: int
    teacher_id: int
    is_passed: bool
    credit_date: date
    attempt_number: int = 1
    comment: Optional[str] = None

class CreditCreateRequestSchema(CreditBase): pass
class CreditUpdateRequestSchema(CreditBase):
    __annotations__ = {k: Optional[v] for k, v in CreditBase.__annotations__.items()}
class CreditReadResponseSchema(CreditBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

# Analytics schemas
from typing import Dict, List, Any, Optional

class PerformanceStatsSchema(BaseModel):
    total_students: int
    excellent: int
    good: int
    satisfactory: int
    unsatisfactory: int
    quality_percentage: float
    success_rate_percentage: float

class StudentCardSchema(BaseModel):
    student: Dict[str, Any]
    study_group: Optional[str]
    grades_by_semester: Dict[str, List[Dict[str, Any]]]
    credits_by_semester: Dict[str, List[Dict[str, Any]]]
    exams_by_semester: Dict[str, List[Dict[str, Any]]]
