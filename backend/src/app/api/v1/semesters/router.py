from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from app.api.v1.dependencies import check_user_role, get_semester_service
from app.api.v1.schemas import Page
from app.models import UserRole
from app.services import SemesterService
from .schemas import SemesterReadResponseSchema, SemesterCreateRequestSchema, SemesterUpdateRequestSchema

router = APIRouter(prefix="/semesters", tags=["Semesters"])

@router.get("")
async def read_semesters(service: Annotated[SemesterService, Depends(get_semester_service)], page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=100), course_id: Optional[int] = None, is_active: Optional[bool] = None) -> Page[SemesterReadResponseSchema]:
    return await service.get_semesters(size=size, page=page, course_id=course_id, is_active=is_active)

@router.get("/{semester_id}")
async def read_semester(semester_id: int, service: Annotated[SemesterService, Depends(get_semester_service)]) -> SemesterReadResponseSchema:
    return await service.get_semester(semester_id)

@router.post("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN]))])
async def create_semester(request_schema: SemesterCreateRequestSchema, service: Annotated[SemesterService, Depends(get_semester_service)]) -> SemesterReadResponseSchema:
    return await service.create_semester(request_schema.model_dump())

@router.patch("/{semester_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN]))])
async def update_semester(semester_id: int, request_schema: SemesterUpdateRequestSchema, service: Annotated[SemesterService, Depends(get_semester_service)]) -> SemesterReadResponseSchema:
    return await service.update_semester(semester_id, request_schema.model_dump(exclude_unset=True))

@router.delete("/{semester_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN]))])
async def delete_semester(semester_id: int, service: Annotated[SemesterService, Depends(get_semester_service)]): return await service.delete_semester(semester_id)

@router.get("/active/current", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER, UserRole.STUDENT]))])
async def get_active_semester(service: Annotated[SemesterService, Depends(get_semester_service)]) -> Optional[SemesterReadResponseSchema]:
    return await service.get_active_semester()
