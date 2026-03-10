from typing import Annotated, List

from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.users.schemas import UserReadResponseSchema
from app.core import messages
from app.core.security import jwt_security
from app.db.session import get_async_session
from app.models import UserRole
from app.services import (
    UserService,
    AuthService,
    FacultyService,
    DepartmentService,
    StudyDirectionService,
    DisciplineService,
    CurriculumService,
    CourseService,
    SemesterService,
    StudyGroupService,
    StudentService,
    TeacherService,
    AcademicStudentGroupService,
    GradeBookService,
    GradeService,
    CreditService,
    ExamService,
    PerformanceAnalyticsService,
)


def get_auth_service(db_session: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(db_session)


def get_user_service(db_session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(db_session)


def get_faculty_service(db_session: AsyncSession = Depends(get_async_session)) -> FacultyService:
    return FacultyService(db_session)


def get_department_service(db_session: AsyncSession = Depends(get_async_session)) -> DepartmentService:
    return DepartmentService(db_session)


def get_study_direction_service(db_session: AsyncSession = Depends(get_async_session)) -> StudyDirectionService:
    return StudyDirectionService(db_session)


def get_discipline_service(db_session: AsyncSession = Depends(get_async_session)) -> DisciplineService:
    return DisciplineService(db_session)


def get_curriculum_service(db_session: AsyncSession = Depends(get_async_session)) -> CurriculumService:
    return CurriculumService(db_session)


def get_course_service(db_session: AsyncSession = Depends(get_async_session)) -> CourseService:
    return CourseService(db_session)


def get_semester_service(db_session: AsyncSession = Depends(get_async_session)) -> SemesterService:
    return SemesterService(db_session)


def get_study_group_service(db_session: AsyncSession = Depends(get_async_session)) -> StudyGroupService:
    return StudyGroupService(db_session)


def get_academic_student_group_service(db_session: AsyncSession = Depends(get_async_session)) -> AcademicStudentGroupService:
    return AcademicStudentGroupService(db_session)


def get_student_service(db_session: AsyncSession = Depends(get_async_session)) -> StudentService:
    return StudentService(db_session)


def get_teacher_service(db_session: AsyncSession = Depends(get_async_session)) -> TeacherService:
    return TeacherService(db_session)


def get_gradebook_service(db_session: AsyncSession = Depends(get_async_session)) -> GradeBookService:
    return GradeBookService(db_session)


def get_grade_service(db_session: AsyncSession = Depends(get_async_session)) -> GradeService:
    return GradeService(db_session)


def get_credit_service(db_session: AsyncSession = Depends(get_async_session)) -> CreditService:
    return CreditService(db_session)


def get_exam_service(db_session: AsyncSession = Depends(get_async_session)) -> ExamService:
    return ExamService(db_session)


def get_performance_analytics_service(db_session: AsyncSession = Depends(get_async_session)) -> PerformanceAnalyticsService:
    return PerformanceAnalyticsService(db_session)


async def get_current_user(
        request: Request,
        user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadResponseSchema:
    access_token = await jwt_security.get_access_token_from_request(
        request,
        locations=["headers"],
    )
    access_token_payload = jwt_security.verify_token(access_token, verify_csrf=False)
    return await user_service.get_user(int(access_token_payload.sub))


def check_user_role(roles: List[UserRole]):
    def role_checker(
            current_user: Annotated[UserReadResponseSchema, Depends(get_current_user)]) -> UserReadResponseSchema:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail=messages.ERROR_USER_HAVE_NOT_ENOUGH_RIGHTS
            )
        return current_user

    return role_checker


__all__ = (
    "get_auth_service",
    "get_user_service",
    "get_faculty_service",
    "get_department_service",
    "get_study_direction_service",
    "get_discipline_service",
    "get_curriculum_service",
    "get_course_service",
    "get_semester_service",
    "get_study_group_service",
    "get_academic_student_group_service",
    "get_student_service",
    "get_teacher_service",
    "get_gradebook_service",
    "get_grade_service",
    "get_credit_service",
    "get_exam_service",
    "get_performance_analytics_service",
    "check_user_role",
    "get_current_user",
)
