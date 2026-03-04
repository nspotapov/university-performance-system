from enum import Enum


class GradeValue(str, Enum):
    # Экзаменационные оценки
    EXCELLENT = "5"
    GOOD = "4"
    SATISFACTORY = "3"
    UNSATISFACTORY = "2"
    # Зачеты
    PASSED = "PASSED"  # Зачтено
    NOT_PASSED = "FAILED"  # Не зачтено
    # Прочее
    ABSENT = "ABSENT"  # Неявка
