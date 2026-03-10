from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from app.api.v1.dependencies import check_user_role, get_curriculum_service
from app.api.v1.schemas import Page
from app.models import UserRole
from app.services import CurriculumService
from .schemas import CurriculumReadResponseSchema, CurriculumCreateRequestSchema, CurriculumUpdateRequestSchema

router = APIRouter(prefix="/curricula", tags=["Curricula"])

@router.get("")
async def read_curricula(service: Annotated[CurriculumService, Depends(get_curriculum_service)], page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=100), study_direction_id: Optional[int] = None) -> Page[CurriculumReadResponseSchema]:
    return await service.get_curricula(size=size, page=page, study_direction_id=study_direction_id)

@router.get("/{curriculum_id}")
async def read_curriculum(curriculum_id: int, service: Annotated[CurriculumService, Depends(get_curriculum_service)]) -> CurriculumReadResponseSchema:
    return await service.get_curriculum(curriculum_id)

@router.post("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN]))])
async def create_curriculum(request_schema: CurriculumCreateRequestSchema, service: Annotated[CurriculumService, Depends(get_curriculum_service)]) -> CurriculumReadResponseSchema:
    return await service.create_curriculum(request_schema.model_dump())

@router.patch("/{curriculum_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN]))])
async def update_curriculum(curriculum_id: int, request_schema: CurriculumUpdateRequestSchema, service: Annotated[CurriculumService, Depends(get_curriculum_service)]) -> CurriculumReadResponseSchema:
    return await service.update_curriculum(curriculum_id, request_schema.model_dump(exclude_unset=True))

@router.delete("/{curriculum_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN]))])
async def delete_curriculum(curriculum_id: int, service: Annotated[CurriculumService, Depends(get_curriculum_service)]): return await service.delete_curriculum(curriculum_id)
