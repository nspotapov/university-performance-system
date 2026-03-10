from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from app.api.v1.dependencies import check_user_role, get_gradebook_service
from app.api.v1.schemas import Page
from app.models import UserRole
from app.services import GradeBookService
from .schemas import GradeBookReadResponseSchema, GradeBookCreateRequestSchema, GradeBookUpdateRequestSchema

router = APIRouter(prefix="/gradebooks", tags=["GradeBooks"])

@router.get("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER]))])
async def read_gradebooks(service: Annotated[GradeBookService, Depends(get_gradebook_service)], page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=100), semester_id: Optional[int] = None, study_group_id: Optional[int] = None, discipline_id: Optional[int] = None, teacher_id: Optional[int] = None, is_closed: Optional[bool] = None) -> Page[GradeBookReadResponseSchema]:
    return await service.get_gradebooks(size=size, page=page, semester_id=semester_id, study_group_id=study_group_id, discipline_id=discipline_id, teacher_id=teacher_id, is_closed=is_closed)

@router.get("/{gradebook_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER]))])
async def read_gradebook(gradebook_id: int, service: Annotated[GradeBookService, Depends(get_gradebook_service)]) -> GradeBookReadResponseSchema:
    return await service.get_gradebook(gradebook_id)

@router.post("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER]))])
async def create_gradebook(request_schema: GradeBookCreateRequestSchema, service: Annotated[GradeBookService, Depends(get_gradebook_service)]) -> GradeBookReadResponseSchema:
    return await service.create_gradebook(request_schema.model_dump())

@router.patch("/{gradebook_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER]))])
async def update_gradebook(gradebook_id: int, request_schema: GradeBookUpdateRequestSchema, service: Annotated[GradeBookService, Depends(get_gradebook_service)]) -> GradeBookReadResponseSchema:
    return await service.update_gradebook(gradebook_id, request_schema.model_dump(exclude_unset=True))

@router.delete("/{gradebook_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER]))])
async def delete_gradebook(gradebook_id: int, service: Annotated[GradeBookService, Depends(get_gradebook_service)]): return await service.delete_gradebook(gradebook_id)
