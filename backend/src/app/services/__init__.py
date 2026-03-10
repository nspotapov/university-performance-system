from .auth import AuthService
from .user import UserService
from .university import (
    FacultyService,
    DepartmentService,
    StudyDirectionService,
    DisciplineService,
    CurriculumService,
    CourseService,
    SemesterService,
    StudyGroupService,
)
from .academic import (
    StudentService,
    TeacherService,
    StudentGroupService as AcademicStudentGroupService,
    GradeBookService,
    GradeService,
    CreditService,
    ExamService,
    PerformanceAnalyticsService,
)

__all__ = (
    "AuthService",
    "UserService",
    "FacultyService",
    "DepartmentService",
    "StudyDirectionService",
    "DisciplineService",
    "CurriculumService",
    "CourseService",
    "SemesterService",
    "StudyGroupService",
    "StudentService",
    "TeacherService",
    "AcademicStudentGroupService",
    "GradeBookService",
    "GradeService",
    "CreditService",
    "ExamService",
    "PerformanceAnalyticsService",
)
