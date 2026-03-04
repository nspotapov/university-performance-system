from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.models import BaseDbModelWithId


class Group(BaseDbModelWithId):
    """Учебная группа"""
    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)  # ИВТ-101
    curriculum_id: Mapped[str] = mapped_column(String, ForeignKey("curriculums.id"))
    current_semester = mapped_column(Integer, default=1)

    students = relationship("StudentProfile", back_populates="group")


class StudentProfile(BaseDbModelWithId):
    """Дополнительные данные студента"""
    __tablename__ = "student_profiles"

    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), primary_key=True)
    group_id: Mapped[str] = mapped_column(String, ForeignKey("groups.id"))
    student_card_number: Mapped[str] = mapped_column(String(50), unique=True)  # Номер зачетки

    user = relationship("User")
    group = relationship("Group", back_populates="students")
