from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query, Response
from app.api.v1.dependencies import check_user_role, get_performance_analytics_service
from app.models import UserRole
from app.services import PerformanceAnalyticsService
from .schemas import PerformanceStatsSchema, StudentCardSchema
import json

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/performance/faculty/{faculty_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN]))])
async def get_faculty_performance(faculty_id: int, semester_id: int, service: Annotated[PerformanceAnalyticsService, Depends(get_performance_analytics_service)]) -> PerformanceStatsSchema:
    result = await service.get_faculty_performance(faculty_id=faculty_id, semester_id=semester_id)
    return PerformanceStatsSchema(**result)

@router.get("/performance/direction/{direction_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER]))])
async def get_direction_performance(direction_id: int, semester_id: int, service: Annotated[PerformanceAnalyticsService, Depends(get_performance_analytics_service)]) -> PerformanceStatsSchema:
    result = await service.get_study_direction_performance(direction_id=direction_id, semester_id=semester_id)
    return PerformanceStatsSchema(**result)

@router.get("/performance/course/{course_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER]))])
async def get_course_performance(course_id: int, semester_id: int, service: Annotated[PerformanceAnalyticsService, Depends(get_performance_analytics_service)]) -> PerformanceStatsSchema:
    result = await service.get_course_performance(course_id=course_id, semester_id=semester_id)
    return PerformanceStatsSchema(**result)

@router.get("/performance/group/{group_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER]))])
async def get_group_performance(group_id: int, semester_id: int, service: Annotated[PerformanceAnalyticsService, Depends(get_performance_analytics_service)]) -> PerformanceStatsSchema:
    result = await service.get_group_performance(group_id=group_id, semester_id=semester_id)
    return PerformanceStatsSchema(**result)

@router.get("/student/{student_id}/card", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER, UserRole.STUDENT]))])
async def get_student_card(student_id: int, service: Annotated[PerformanceAnalyticsService, Depends(get_performance_analytics_service)], format: Optional[str] = Query("json")) -> StudentCardSchema:
    result = await service.get_student_card(student_id=student_id)
    return StudentCardSchema(**result)

@router.get("/student/{student_id}/card/print", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER, UserRole.STUDENT]))])
async def print_student_card(student_id: int, service: Annotated[PerformanceAnalyticsService, Depends(get_performance_analytics_service)]):
    result = await service.get_student_card(student_id=student_id)
    # Возвращаем HTML для печати
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Карточка студента</title><style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ text-align: center; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        @media print {{ body {{ margin: 0; }} }}
    </style></head>
    <body>
        <h1>Карточка успеваемости студента</h1>
        <p><strong>ФИО:</strong> {result['student']['last_name']} {result['student']['first_name']} {result['student']['middle_name'] or ''}</p>
        <p><strong>Дата рождения:</strong> {result['student']['birth_date']}</p>
        <p><strong>Год поступления:</strong> {result['student']['enrollment_year']}</p>
        <p><strong>Группа:</strong> {result['study_group'] or 'Не указана'}</p>
        <h2>Оценки по семестрам</h2>
    """
    for semester, grades in result['grades_by_semester'].items():
        html_content += f"<h3>{semester}</h3><table><tr><th>Дисциплина</th><th>Оценка</th><th>Тип</th><th>Дата</th></tr>"
        for grade in grades:
            html_content += f"<tr><td>{grade['discipline']}</td><td>{grade['grade']}</td><td>{grade['type']}</td><td>{grade['date']}</td></tr>"
        html_content += "</table>"
    html_content += """</body></html>"""
    return Response(content=html_content, media_type="text/html")
