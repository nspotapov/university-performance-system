from datetime import date
from enum import StrEnum

from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class GradeType(StrEnum):
    """Типы оценок"""
    EXAM = "EXAM"  # Экзамен
    CREDIT = "CREDIT"  # Зачет
    COURSEWORK = "COURSEWORK"  # Курсовая работа
    TEST = "TEST"  # Тест/контрольная


class GradeValue(StrEnum):
    """Значения оценок (5-балльная шкала)"""
    EXCELLENT = "5"  # Отлично
    GOOD = "4"  # Хорошо
    SATISFACTORY = "3"  # Удовлетворительно
    UNSATISFACTORY = "2"  # Неудовлетворительно
    PASS = "PASS"  # Зачтено
    FAIL = "FAIL"  # Не зачтено


class Student(Base):
    """Студент"""
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, unique=True)
    first_name: Mapped[str]  # Имя
    last_name: Mapped[str]  # Фамилия
    middle_name: Mapped[str | None]  # Отчество
    birth_date: Mapped[date]  # Дата рождения
    enrollment_year: Mapped[int]  # Год поступления
    is_expelled: Mapped[bool] = mapped_column(default=False)  # Отчислен ли
    expulsion_reason: Mapped[str | None]  # Причина отчисления
    description: Mapped[str | None]


class Teacher(Base):
    """Преподаватель"""
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, unique=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), index=True)
    first_name: Mapped[str]  # Имя
    last_name: Mapped[str]  # Фамилия
    middle_name: Mapped[str | None]  # Отчество
    position: Mapped[str]  # Должность (доцент, профессор и т.д.)
    academic_degree: Mapped[str | None]  # Ученая степень
    academic_title: Mapped[str | None]  # Ученое звание
    hire_date: Mapped[date]  # Дата приема на работу
    is_fired: Mapped[bool] = mapped_column(default=False)  # Уволен ли
    description: Mapped[str | None]


class StudentGroup(Base):
    """Связь студента с учебной группой"""
    __tablename__ = "student_groups"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    study_group_id: Mapped[int] = mapped_column(ForeignKey("study_groups.id"), index=True)
    start_date: Mapped[date]  # Дата зачисления в группу
    end_date: Mapped[date | None]  # Дата выбытия из группы
    is_current: Mapped[bool] = mapped_column(default=True)  # Текущая ли группа

    __table_args__ = (
        UniqueConstraint('student_id', 'study_group_id', name='uq_student_study_group'),
    )


class GradeBook(Base):
    """Ведомость оценок"""
    __tablename__ = "gradebooks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    semester_id: Mapped[int] = mapped_column(ForeignKey("semesters.id"), index=True)
    study_group_id: Mapped[int] = mapped_column(ForeignKey("study_groups.id"), index=True)
    discipline_id: Mapped[int] = mapped_column(ForeignKey("disciplines.id"), index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), index=True)
    grade_type: Mapped[GradeType]  # Тип ведомости (экзамен/зачет)
    name: Mapped[str]  # Название ведомости
    created_at: Mapped[date]  # Дата создания
    is_closed: Mapped[bool] = mapped_column(default=False)  # Закрыта ли ведомость

    __table_args__ = (
        UniqueConstraint(
            'semester_id', 'study_group_id', 'discipline_id', 'teacher_id',
            name='uq_gradebook_semester_group_discipline_teacher'
        ),
    )


class Grade(Base):
    """Оценка студента"""
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    gradebook_id: Mapped[int] = mapped_column(ForeignKey("gradebooks.id"), index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    grade_value: Mapped[GradeValue]  # Значение оценки
    grade_date: Mapped[date]  # Дата выставления
    comment: Mapped[str | None]  # Комментарий преподавателя

    __table_args__ = (
        UniqueConstraint('gradebook_id', 'student_id', name='uq_grade_gradebook_student'),
    )


class Credit(Base):
    """Зачет"""
    __tablename__ = "credits"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    discipline_id: Mapped[int] = mapped_column(ForeignKey("disciplines.id"), index=True)
    semester_id: Mapped[int] = mapped_column(ForeignKey("semesters.id"), index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), index=True)
    is_passed: Mapped[bool]  # Сдан ли зачет
    credit_date: Mapped[date]  # Дата сдачи
    attempt_number: Mapped[int] = mapped_column(default=1)  # Номер попытки
    comment: Mapped[str | None]

    __table_args__ = (
        UniqueConstraint(
            'student_id', 'discipline_id', 'semester_id', 'attempt_number',
            name='uq_credit_student_discipline_semester_attempt'
        ),
    )


class Exam(Base):
    """Экзамен"""
    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    discipline_id: Mapped[int] = mapped_column(ForeignKey("disciplines.id"), index=True)
    semester_id: Mapped[int] = mapped_column(ForeignKey("semesters.id"), index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), index=True)
    grade_value: Mapped[GradeValue]  # Оценка за экзамен
    exam_date: Mapped[date]  # Дата экзамена
    attempt_number: Mapped[int] = mapped_column(default=1)  # Номер попытки
    comment: Mapped[str | None]

    __table_args__ = (
        UniqueConstraint(
            'student_id', 'discipline_id', 'semester_id', 'attempt_number',
            name='uq_exam_student_discipline_semester_attempt'
        ),
        CheckConstraint('grade_value IN (\'5\', \'4\', \'3\', \'2\')', name='check_exam_grade_value'),
    )
