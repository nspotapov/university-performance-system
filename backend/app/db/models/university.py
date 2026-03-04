from sqlalchemy import Integer, String, ForeignKey, Table, Enum, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column

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

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    short_name: Mapped[str] = mapped_column(String(20))  # Например, ИТПИ

    departments = relationship("Department", back_populates="faculty")


class Department(BaseDbModelWithId):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    faculty_id: Mapped[str] = mapped_column(String(36), ForeignKey("faculties.id"))

    faculty = relationship("Faculty", back_populates="departments")
    directions = relationship("Direction", back_populates="department")
    subjects = relationship("Subject", back_populates="department")


class Direction(BaseDbModelWithId):
    """Направления обучения (например, 09.03.04 Программная инженерия)"""
    __tablename__ = "directions"

    code: Mapped[str] = mapped_column(String(20), nullable=False)  # Код специальности
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    department_id: Mapped[str] = mapped_column(String(36), ForeignKey("departments.id"))

    department = relationship("Department", back_populates="directions")
    curriculums = relationship("Curriculum", back_populates="direction")


class Subject(BaseDbModelWithId):
    """Дисциплины"""
    __tablename__ = "subjects"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    department_id: Mapped[str] = mapped_column(String(36), ForeignKey("departments.id"))

    department = relationship("Department", back_populates="subjects")
    teachers = relationship("User", secondary="teacher_subjects")


class Curriculum(BaseDbModelWithId):
    """Учебный план для направления"""
    __tablename__ = "curriculums"

    direction_id: Mapped[str] = mapped_column(String(36), ForeignKey("directions.id"))
    year_start: Mapped[int] = mapped_column(Integer, nullable=False)  # Год набора

    direction = relationship("Direction", back_populates="curriculums")
    items = relationship("CurriculumItem", back_populates="curriculum")


class CurriculumItem(BaseDbModelWithId):
    """Конкретный предмет в учебном плане (семестр, часы, тип контроля)"""
    __tablename__ = "curriculum_items"

    curriculum_id: Mapped[str] = mapped_column(String(36), ForeignKey("curriculums.id"))
    subject_id: Mapped[str] = mapped_column(String(36), ForeignKey("subjects.id"))
    semester: Mapped[int] = mapped_column(Integer, nullable=False)
    hours: Mapped[int] = mapped_column(Integer)
    control_type: Mapped[ControlType] = mapped_column(Enum(ControlType), nullable=False)

    curriculum = relationship("Curriculum", back_populates="items")
    subject = relationship("Subject")
