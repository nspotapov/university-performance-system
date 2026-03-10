from .user import UserRepository
from .university import (
    FacultyRepository,
    DepartmentRepository,
    StudyDirectionRepository,
    DisciplineRepository,
    CurriculumRepository,
    CourseRepository,
    SemesterRepository,
    StudyGroupRepository,
)
from .academic import (
    StudentRepository,
    TeacherRepository,
    StudentGroupRepository,
    GradeBookRepository,
    GradeRepository,
    CreditRepository,
    ExamRepository,
)

__all__ = (
    "UserRepository",
    "FacultyRepository",
    "DepartmentRepository",
    "StudyDirectionRepository",
    "DisciplineRepository",
    "CurriculumRepository",
    "CourseRepository",
    "SemesterRepository",
    "StudyGroupRepository",
    "StudentRepository",
    "TeacherRepository",
    "StudentGroupRepository",
    "GradeBookRepository",
    "GradeRepository",
    "CreditRepository",
    "ExamRepository",
)
