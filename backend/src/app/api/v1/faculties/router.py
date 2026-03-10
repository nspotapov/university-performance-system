from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.v1.dependencies import check_user_role, get_faculty_service
from app.api.v1.schemas import Page
from app.api.v1.university.schemas import FacultyReadResponseSchema, FacultyCreateRequestSchema, FacultyUpdateRequestSchema
from app.models import UserRole
from app.services import FacultyService

router = APIRouter(prefix="/faculties", tags=["Faculties"])

@router.get("")
async def read_faculties(
    faculty_service: Annotated[FacultyService, Depends(get_faculty_service)],
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
) -> Page[FacultyReadResponseSchema]:
    return await faculty_service.get_faculties(size=size, page=page)

@router.get("/{faculty_id}")
async def read_faculty(
    faculty_id: int,
    faculty_service: Annotated[FacultyService, Depends(get_faculty_service)]
) -> FacultyReadResponseSchema:
    return await faculty_service.get_faculty(faculty_id)

@router.post("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN]))])
async def create_faculty(
    request_schema: FacultyCreateRequestSchema,
    faculty_service: Annotated[FacultyService, Depends(get_faculty_service)],
) -> FacultyReadResponseSchema:
    return await faculty_service.create_faculty(request_schema.model_dump())

@router.patch("/{faculty_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN]))])
async def update_faculty(
    faculty_id: int,
    request_schema: FacultyUpdateRequestSchema,
    faculty_service: Annotated[FacultyService, Depends(get_faculty_service)],
) -> FacultyReadResponseSchema:
    return await faculty_service.update_faculty(faculty_id, request_schema.model_dump(exclude_unset=True))

@router.delete("/{faculty_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN]))])
async def delete_faculty(
    faculty_id: int,
    faculty_service: Annotated[FacultyService, Depends(get_faculty_service)],
):
    return await faculty_service.delete_faculty(faculty_id)
