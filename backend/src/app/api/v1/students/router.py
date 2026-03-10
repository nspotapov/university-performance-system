from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from app.api.v1.dependencies import check_user_role, get_student_service
from app.api.v1.schemas import Page
from app.models import UserRole
from app.services import StudentService
from .schemas import StudentReadResponseSchema, StudentCreateRequestSchema, StudentUpdateRequestSchema

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER]))])
async def read_students(service: Annotated[StudentService, Depends(get_student_service)], page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=100), user_id: Optional[int] = None, is_expelled: Optional[bool] = None) -> Page[StudentReadResponseSchema]:
    return await service.get_students(size=size, page=page, user_id=user_id, is_expelled=is_expelled)

@router.get("/{student_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER, UserRole.STUDENT]))])
async def read_student(student_id: int, service: Annotated[StudentService, Depends(get_student_service)]) -> StudentReadResponseSchema:
    return await service.get_student(student_id)

@router.post("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN]))])
async def create_student(request_schema: StudentCreateRequestSchema, service: Annotated[StudentService, Depends(get_student_service)]) -> StudentReadResponseSchema:
    return await service.create_student(request_schema.model_dump())

@router.patch("/{student_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN]))])
async def update_student(student_id: int, request_schema: StudentUpdateRequestSchema, service: Annotated[StudentService, Depends(get_student_service)]) -> StudentReadResponseSchema:
    return await service.update_student(student_id, request_schema.model_dump(exclude_unset=True))

@router.delete("/{student_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN]))])
async def delete_student(student_id: int, service: Annotated[StudentService, Depends(get_student_service)]): return await service.delete_student(student_id)
