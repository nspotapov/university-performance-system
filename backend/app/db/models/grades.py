from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.enums import GradeValue
from app.db.models import BaseDbModelWithId


class GradeSheet(BaseDbModelWithId):
    """Электронная ведомость"""
    __tablename__ = "grade_sheets"

    # Связь с предметом из учебного плана (оттуда берем семестр и тип контроля)
    curriculum_item_id = Column(Integer, ForeignKey("curriculum_items.id"), nullable=False)

    # Для какой группы эта ведомость
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)

    # Кто принимает (преподаватель)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Метаданные
    is_closed = Column(Boolean, default=False)  # Если True, оценки менять нельзя
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    curriculum_item = relationship("CurriculumItem")
    group = relationship("Group")
    teacher = relationship("User")
    grades = relationship("Grade", back_populates="sheet", cascade="all, delete-orphan")


class Grade(BaseDbModelWithId):
    """Конкретная оценка студента в ведомости"""
    __tablename__ = "grades"

    sheet_id = Column(Integer, ForeignKey("grade_sheets.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # FK на User (роль Student)

    value = Column(Enum(GradeValue), nullable=False)

    # Для расчета среднего балла и аналитики (например: 5, 4, 3, 2, или 1/0 для зачетов)
    numeric_value = Column(Integer, nullable=True)

    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    sheet = relationship("GradeSheet", back_populates="grades")
    student = relationship("User")

    # Ограничение: один студент — одна оценка в одной ведомости
    __table_args__ = (
        CheckConstraint('numeric_value >= 0 AND numeric_value <= 5', name='check_grade_range'),
    )
