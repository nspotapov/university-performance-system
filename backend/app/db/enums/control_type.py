from enum import StrEnum


class ControlType(StrEnum):
    EXAM = "EXAM"  # Экзамен
    CREDIT = "CREDIT"  # Зачет
    GRADED_CREDIT = "GRADED"  # Дифференцированный зачет
