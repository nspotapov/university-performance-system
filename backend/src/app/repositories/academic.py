from app.models import (
    Student,
    Teacher,
    StudentGroup,
    GradeBook,
    Grade,
    Credit,
    Exam,
)
from .sqlalchemy import SQLAlchemyRepository


class StudentRepository(SQLAlchemyRepository[Student]):
    model = Student


class TeacherRepository(SQLAlchemyRepository[Teacher]):
    model = Teacher


class StudentGroupRepository(SQLAlchemyRepository[StudentGroup]):
    model = StudentGroup


class GradeBookRepository(SQLAlchemyRepository[GradeBook]):
    model = GradeBook


class GradeRepository(SQLAlchemyRepository[Grade]):
    model = Grade


class CreditRepository(SQLAlchemyRepository[Credit]):
    model = Credit


class ExamRepository(SQLAlchemyRepository[Exam]):
    model = Exam
