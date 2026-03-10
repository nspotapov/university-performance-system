from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from app.api.v1.dependencies import check_user_role, get_study_group_service
from app.api.v1.schemas import Page
from app.api.v1.university.schemas import StudyGroupReadResponseSchema, StudyGroupCreateRequestSchema, StudyGroupUpdateRequestSchema
from app.models import UserRole
from app.services import StudyGroupService

router = APIRouter(prefix="/study-groups", tags=["Study Groups"])

@router.get("")
async def read_study_groups(service: Annotated[StudyGroupService, Depends(get_study_group_service)], page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=100), study_direction_id: Optional[int] = None, course_id: Optional[int] = None) -> Page[StudyGroupReadResponseSchema]:
    return await service.get_study_groups(size=size, page=page, study_direction_id=study_direction_id, course_id=course_id)

@router.get("/{group_id}")
async def read_study_group(group_id: int, service: Annotated[StudyGroupService, Depends(get_study_group_service)]) -> StudyGroupReadResponseSchema:
    return await service.get_study_group(group_id)

@router.post("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN]))])
async def create_study_group(request_schema: StudyGroupCreateRequestSchema, service: Annotated[StudyGroupService, Depends(get_study_group_service)]) -> StudyGroupReadResponseSchema:
    return await service.create_study_group(request_schema.model_dump())

@router.patch("/{group_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN]))])
async def update_study_group(group_id: int, request_schema: StudyGroupUpdateRequestSchema, service: Annotated[StudyGroupService, Depends(get_study_group_service)]) -> StudyGroupReadResponseSchema:
    return await service.update_study_group(group_id, request_schema.model_dump(exclude_unset=True))

@router.delete("/{group_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN]))])
async def delete_study_group(group_id: int, service: Annotated[StudyGroupService, Depends(get_study_group_service)]): return await service.delete_study_group(group_id)
