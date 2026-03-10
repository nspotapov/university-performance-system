from enum import StrEnum

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Faculty(Base):
    """Факультет университета"""
    __tablename__ = "faculties"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str]  # Название факультета
    short_name: Mapped[str]  # Краткое название (аббревиатура)
    description: Mapped[str | None]  # Описание


class Department(Base):
    """Кафедра факультета"""
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"), index=True)
    name: Mapped[str]  # Название кафедры
    short_name: Mapped[str]  # Краткое название
    description: Mapped[str | None]  # Описание


class StudyDirection(Base):
    """Направление обучения (специальность)"""
    __tablename__ = "study_directions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"), index=True)
    name: Mapped[str]  # Название направления
    code: Mapped[str]  # Код направления (например, "09.03.01")
    level: Mapped[str]  # Уровень: бакалавриат, магистратура, специалитет
    description: Mapped[str | None]  # Описание


class Discipline(Base):
    """Учебная дисциплина"""
    __tablename__ = "disciplines"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    study_direction_id: Mapped[int] = mapped_column(ForeignKey("study_directions.id"), index=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), index=True)
    name: Mapped[str]  # Название дисциплины
    code: Mapped[str]  # Код дисциплины
    hours: Mapped[int]  # Количество часов
    description: Mapped[str | None]  # Описание


class Curriculum(Base):
    """Учебный план"""
    __tablename__ = "curricula"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    study_direction_id: Mapped[int] = mapped_column(ForeignKey("study_directions.id"), index=True)
    name: Mapped[str]  # Название учебного плана
    year: Mapped[int]  # Год утверждения
    description: Mapped[str | None]  # Описание


class Course(Base):
    """Курс обучения (1-6 курс)"""
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    number: Mapped[int] = mapped_column(unique=True)  # Номер курса (1-6)
    description: Mapped[str | None]


class Semester(Base):
    """Семестр обучения"""
    __tablename__ = "semesters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), index=True)
    number: Mapped[int]  # Номер семестра (1-12)
    name: Mapped[str]  # Название (например, "Осенний семестр 2025")
    start_date: Mapped[str]  # Дата начала
    end_date: Mapped[str]  # Дата окончания
    is_active: Mapped[bool] = mapped_column(default=False)  # Активный ли семестр

    __table_args__ = (
        UniqueConstraint('course_id', 'number', name='uq_semester_course_number'),
    )


class StudyGroup(Base):
    """Учебная группа студентов"""
    __tablename__ = "study_groups"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    study_direction_id: Mapped[int] = mapped_column(ForeignKey("study_directions.id"), index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), index=True)
    name: Mapped[str]  # Название группы (например, "ИВТ-301")
    year: Mapped[int]  # Год набора
    description: Mapped[str | None]
