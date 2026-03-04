from .user_model import User
from .base_model import BaseDbModel, BaseDbModelWithId
from .otp_model import OTP
from .university import Faculty, Department, Direction, Subject, Curriculum, CurriculumItem
from .academic import StudentProfile, Group

__all__ = [
    "User",
    "BaseDbModelWithId",
    "BaseDbModel",
    "OTP",
    "Faculty",
    "Department",
    "Direction",
    "Subject",
    "Curriculum",
    "CurriculumItem",
    "StudentProfile",
    "Group",
]
