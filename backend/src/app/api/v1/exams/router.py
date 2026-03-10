from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from app.api.v1.dependencies import check_user_role, get_exam_service
from app.api.v1.schemas import Page
from app.models import UserRole
from app.services import ExamService
from .schemas import ExamReadResponseSchema, ExamCreateRequestSchema, ExamUpdateRequestSchema

router = APIRouter(prefix="/exams", tags=["Exams"])

@router.get("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER, UserRole.STUDENT]))])
async def read_exams(service: Annotated[ExamService, Depends(get_exam_service)], page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=100), student_id: Optional[int] = None, discipline_id: Optional[int] = None, semester_id: Optional[int] = None, teacher_id: Optional[int] = None) -> Page[ExamReadResponseSchema]:
    return await service.get_exams(size=size, page=page, student_id=student_id, discipline_id=discipline_id, semester_id=semester_id, teacher_id=teacher_id)

@router.get("/{exam_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER, UserRole.STUDENT]))])
async def read_exam(exam_id: int, service: Annotated[ExamService, Depends(get_exam_service)]) -> ExamReadResponseSchema:
    return await service.get_exam(exam_id)

@router.post("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER]))])
async def create_exam(request_schema: ExamCreateRequestSchema, service: Annotated[ExamService, Depends(get_exam_service)]) -> ExamReadResponseSchema:
    return await service.create_exam(request_schema.model_dump())

@router.patch("/{exam_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER]))])
async def update_exam(exam_id: int, request_schema: ExamUpdateRequestSchema, service: Annotated[ExamService, Depends(get_exam_service)]) -> ExamReadResponseSchema:
    return await service.update_exam(exam_id, request_schema.model_dump(exclude_unset=True))

@router.delete("/{exam_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER]))])
async def delete_exam(exam_id: int, service: Annotated[ExamService, Depends(get_exam_service)]): return await service.delete_exam(exam_id)
