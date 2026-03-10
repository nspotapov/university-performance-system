from app.models import (
    Faculty,
    Department,
    StudyDirection,
    Discipline,
    Curriculum,
    Course,
    Semester,
    StudyGroup,
)
from .sqlalchemy import SQLAlchemyRepository


class FacultyRepository(SQLAlchemyRepository[Faculty]):
    model = Faculty


class DepartmentRepository(SQLAlchemyRepository[Department]):
    model = Department


class StudyDirectionRepository(SQLAlchemyRepository[StudyDirection]):
    model = StudyDirection


class DisciplineRepository(SQLAlchemyRepository[Discipline]):
    model = Discipline


class CurriculumRepository(SQLAlchemyRepository[Curriculum]):
    model = Curriculum


class CourseRepository(SQLAlchemyRepository[Course]):
    model = Course


class SemesterRepository(SQLAlchemyRepository[Semester]):
    model = Semester


class StudyGroupRepository(SQLAlchemyRepository[StudyGroup]):
    model = StudyGroup
