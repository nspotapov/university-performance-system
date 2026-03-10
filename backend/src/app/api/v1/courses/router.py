from typing import Annotated
from fastapi import APIRouter, Depends, Query
from app.api.v1.dependencies import check_user_role, get_course_service
from app.api.v1.schemas import Page
from app.api.v1.university.schemas import CourseReadResponseSchema, CourseCreateRequestSchema, CourseUpdateRequestSchema
from app.models import UserRole
from app.services import CourseService

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("")
async def read_courses(service: Annotated[CourseService, Depends(get_course_service)], page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=100)) -> Page[CourseReadResponseSchema]:
    return await service.get_courses(size=size, page=page)

@router.get("/{course_id}")
async def read_course(course_id: int, service: Annotated[CourseService, Depends(get_course_service)]) -> CourseReadResponseSchema:
    return await service.get_course(course_id)

@router.post("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN]))])
async def create_course(request_schema: CourseCreateRequestSchema, service: Annotated[CourseService, Depends(get_course_service)]) -> CourseReadResponseSchema:
    return await service.create_course(request_schema.model_dump())

@router.patch("/{course_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN]))])
async def update_course(course_id: int, request_schema: CourseUpdateRequestSchema, service: Annotated[CourseService, Depends(get_course_service)]) -> CourseReadResponseSchema:
    return await service.update_course(course_id, request_schema.model_dump(exclude_unset=True))

@router.delete("/{course_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN]))])
async def delete_course(course_id: int, service: Annotated[CourseService, Depends(get_course_service)]): return await service.delete_course(course_id)
