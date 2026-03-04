from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    RECTOR = "RECTOR"
    DEAN = "DEAN"
    HEAD_TEACHER = "HEAD_TEACHER"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"
