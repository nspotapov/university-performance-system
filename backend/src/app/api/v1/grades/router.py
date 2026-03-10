from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from app.api.v1.dependencies import check_user_role, get_grade_service
from app.api.v1.schemas import Page
from app.models import UserRole
from app.services import GradeService
from .schemas import GradeReadResponseSchema, GradeCreateRequestSchema, GradeUpdateRequestSchema

router = APIRouter(prefix="/grades", tags=["Grades"])

@router.get("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER, UserRole.STUDENT]))])
async def read_grades(service: Annotated[GradeService, Depends(get_grade_service)], page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=100), gradebook_id: Optional[int] = None, student_id: Optional[int] = None) -> Page[GradeReadResponseSchema]:
    return await service.get_grades(size=size, page=page, gradebook_id=gradebook_id, student_id=student_id)

@router.get("/{grade_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER, UserRole.STUDENT]))])
async def read_grade(grade_id: int, service: Annotated[GradeService, Depends(get_grade_service)]) -> GradeReadResponseSchema:
    return await service.get_grade(grade_id)

@router.post("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER]))])
async def create_grade(request_schema: GradeCreateRequestSchema, service: Annotated[GradeService, Depends(get_grade_service)]) -> GradeReadResponseSchema:
    return await service.create_grade(request_schema.model_dump())

@router.patch("/{grade_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER]))])
async def update_grade(grade_id: int, request_schema: GradeUpdateRequestSchema, service: Annotated[GradeService, Depends(get_grade_service)]) -> GradeReadResponseSchema:
    return await service.update_grade(grade_id, request_schema.model_dump(exclude_unset=True))

@router.delete("/{grade_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER]))])
async def delete_grade(grade_id: int, service: Annotated[GradeService, Depends(get_grade_service)]): return await service.delete_grade(grade_id)
