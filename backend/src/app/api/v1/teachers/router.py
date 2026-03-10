from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from app.api.v1.dependencies import check_user_role, get_teacher_service
from app.api.v1.schemas import Page
from app.models import UserRole
from app.services import TeacherService
from .schemas import TeacherReadResponseSchema, TeacherCreateRequestSchema, TeacherUpdateRequestSchema

router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.get("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER]))])
async def read_teachers(service: Annotated[TeacherService, Depends(get_teacher_service)], page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=100), user_id: Optional[int] = None, department_id: Optional[int] = None, is_fired: Optional[bool] = None) -> Page[TeacherReadResponseSchema]:
    return await service.get_teachers(size=size, page=page, user_id=user_id, department_id=department_id, is_fired=is_fired)

@router.get("/{teacher_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER]))])
async def read_teacher(teacher_id: int, service: Annotated[TeacherService, Depends(get_teacher_service)]) -> TeacherReadResponseSchema:
    return await service.get_teacher(teacher_id)

@router.post("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER]))])
async def create_teacher(request_schema: TeacherCreateRequestSchema, service: Annotated[TeacherService, Depends(get_teacher_service)]) -> TeacherReadResponseSchema:
    return await service.create_teacher(request_schema.model_dump())

@router.patch("/{teacher_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER]))])
async def update_teacher(teacher_id: int, request_schema: TeacherUpdateRequestSchema, service: Annotated[TeacherService, Depends(get_teacher_service)]) -> TeacherReadResponseSchema:
    return await service.update_teacher(teacher_id, request_schema.model_dump(exclude_unset=True))

@router.delete("/{teacher_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN]))])
async def delete_teacher(teacher_id: int, service: Annotated[TeacherService, Depends(get_teacher_service)]): return await service.delete_teacher(teacher_id)
