from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models import BaseDbModelWithId


class Group(BaseDbModelWithId):
    """Учебная группа"""
    __tablename__ = "groups"

    name = Column(String(50), unique=True, nullable=False)  # ИВТ-101
    curriculum_id = Column(Integer, ForeignKey("curriculums.id"))
    current_semester = Column(Integer, default=1)

    students = relationship("StudentProfile", back_populates="group")


class StudentProfile(BaseDbModelWithId):
    """Дополнительные данные студента"""
    __tablename__ = "student_profiles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    student_card_number = Column(String(50), unique=True)  # Номер зачетки

    user = relationship("User")
    group = relationship("Group", back_populates="students")
