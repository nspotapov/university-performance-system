from .base import Base
from .user import User, UserRole, MFAMethod
from .university import (
    Faculty,
    Department,
    StudyDirection,
    Discipline,
    Curriculum,
    Course,
    Semester,
    StudyGroup,
)
from .academic import (
    Student,
    Teacher,
    StudentGroup,
    GradeBook,
    Grade,
    Credit,
    Exam,
    GradeType,
    GradeValue,
)

__all__ = (
    "Base",
    "User",
    "UserRole",
    "MFAMethod",
    "Faculty",
    "Department",
    "StudyDirection",
    "Discipline",
    "Curriculum",
    "Course",
    "Semester",
    "StudyGroup",
    "Student",
    "Teacher",
    "StudentGroup",
    "GradeBook",
    "Grade",
    "Credit",
    "Exam",
    "GradeType",
    "GradeValue",
)
