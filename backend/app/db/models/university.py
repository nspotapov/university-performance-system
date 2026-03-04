from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship

from app.db.enums import ControlType
from app.db.models import BaseDbModelWithId, BaseDbModel

# Промежуточная таблица для связи "Преподаватель - Дисциплина"
teacher_subjects = Table(
    "teacher_subjects",
    BaseDbModel.metadata,
    Column("teacher_id", ForeignKey("users.id"), primary_key=True),
    Column("subject_id", ForeignKey("subjects.id"), primary_key=True),
)


class Faculty(BaseDbModelWithId):
    __tablename__ = "faculties"

    name = Column(String(255), unique=True, nullable=False)
    short_name = Column(String(20))  # Например, ИТПИ

    departments = relationship("Department", back_populates="faculty")


class Department(BaseDbModelWithId):
    __tablename__ = "departments"

    name = Column(String(255), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"))

    faculty = relationship("Faculty", back_populates="departments")
    directions = relationship("Direction", back_populates="department")
    subjects = relationship("Subject", back_populates="department")


class Direction(BaseDbModelWithId):
    """Направления обучения (например, 09.03.04 Программная инженерия)"""
    __tablename__ = "directions"

    code = Column(String(20), nullable=False)  # Код специальности
    name = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department", back_populates="directions")
    curriculums = relationship("Curriculum", back_populates="direction")


class Subject(BaseDbModelWithId):
    """Дисциплины"""
    __tablename__ = "subjects"

    name = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department", back_populates="subjects")
    teachers = relationship("User", secondary=teacher_subjects)


class Curriculum(BaseDbModelWithId):
    """Учебный план для направления"""
    __tablename__ = "curriculums"

    direction_id = Column(Integer, ForeignKey("directions.id"))
    year_start = Column(Integer, nullable=False)  # Год набора

    direction = relationship("Direction", back_populates="curriculums")
    items = relationship("CurriculumItem", back_populates="curriculum")


class CurriculumItem(BaseDbModelWithId):
    """Конкретный предмет в учебном плане (семестр, часы, тип контроля)"""
    __tablename__ = "curriculum_items"

    curriculum_id = Column(Integer, ForeignKey("curriculums.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    semester = Column(Integer, nullable=False)
    hours = Column(Integer)
    control_type = Column(Enum(ControlType), nullable=False)

    curriculum = relationship("Curriculum", back_populates="items")
    subject = relationship("Subject")
