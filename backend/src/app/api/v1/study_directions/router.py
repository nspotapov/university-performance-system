from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from app.api.v1.dependencies import check_user_role
from app.api.v1.schemas import Page
from app.api.v1.university.schemas import StudyDirectionReadResponseSchema, StudyDirectionCreateRequestSchema, StudyDirectionUpdateRequestSchema
from app.models import UserRole
from app.services import StudyDirectionService

router = APIRouter(prefix="/study-directions", tags=["Study Directions"])

@router.get("")
async def read_study_directions(
    service: Annotated[StudyDirectionService, Depends()],
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    faculty_id: Optional[int] = None,
) -> Page[StudyDirectionReadResponseSchema]:
    return await service.get_study_directions(size=size, page=page, faculty_id=faculty_id)

@router.get("/{direction_id}")
async def read_study_direction(
    direction_id: int,
    service: Annotated[StudyDirectionService, Depends()]
) -> StudyDirectionReadResponseSchema:
    return await service.get_study_direction(direction_id)

@router.post("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN]))])
async def create_study_direction(
    request_schema: StudyDirectionCreateRequestSchema,
    service: Annotated[StudyDirectionService, Depends()],
) -> StudyDirectionReadResponseSchema:
    return await service.create_study_direction(request_schema.model_dump())

@router.patch("/{direction_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN]))])
async def update_study_direction(
    direction_id: int,
    request_schema: StudyDirectionUpdateRequestSchema,
    service: Annotated[StudyDirectionService, Depends()],
) -> StudyDirectionReadResponseSchema:
    return await service.update_study_direction(direction_id, request_schema.model_dump(exclude_unset=True))

@router.delete("/{direction_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN]))])
async def delete_study_direction(
    direction_id: int,
    service: Annotated[StudyDirectionService, Depends()],
):
    return await service.delete_study_direction(direction_id)
