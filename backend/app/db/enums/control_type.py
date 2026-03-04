from enum import Enum


class ControlType(str, Enum):
    EXAM = "EXAM"  # Экзамен
    CREDIT = "CREDIT"  # Зачет
    GRADED_CREDIT = "GRADED"  # Дифференцированный зачет
