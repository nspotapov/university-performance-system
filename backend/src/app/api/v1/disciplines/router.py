from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from app.api.v1.dependencies import check_user_role, get_discipline_service
from app.api.v1.schemas import Page
from app.models import UserRole
from app.services import DisciplineService
from .schemas import DisciplineReadResponseSchema, DisciplineCreateRequestSchema, DisciplineUpdateRequestSchema

router = APIRouter(prefix="/disciplines", tags=["Disciplines"])

@router.get("")
async def read_disciplines(service: Annotated[DisciplineService, Depends(get_discipline_service)], page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=100), study_direction_id: Optional[int] = None, department_id: Optional[int] = None) -> Page[DisciplineReadResponseSchema]:
    return await service.get_disciplines(size=size, page=page, study_direction_id=study_direction_id, department_id=department_id)

@router.get("/{discipline_id}")
async def read_discipline(discipline_id: int, service: Annotated[DisciplineService, Depends(get_discipline_service)]) -> DisciplineReadResponseSchema:
    return await service.get_discipline(discipline_id)

@router.post("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER]))])
async def create_discipline(request_schema: DisciplineCreateRequestSchema, service: Annotated[DisciplineService, Depends(get_discipline_service)]) -> DisciplineReadResponseSchema:
    return await service.create_discipline(request_schema.model_dump())

@router.patch("/{discipline_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER]))])
async def update_discipline(discipline_id: int, request_schema: DisciplineUpdateRequestSchema, service: Annotated[DisciplineService, Depends(get_discipline_service)]) -> DisciplineReadResponseSchema:
    return await service.update_discipline(discipline_id, request_schema.model_dump(exclude_unset=True))

@router.delete("/{discipline_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN]))])
async def delete_discipline(discipline_id: int, service: Annotated[DisciplineService, Depends(get_discipline_service)]): return await service.delete_discipline(discipline_id)
