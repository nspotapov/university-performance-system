from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query

from app.api.v1.dependencies import check_user_role, get_department_service
from app.api.v1.schemas import Page
from app.models import UserRole
from app.services import DepartmentService
from .schemas import DepartmentReadResponseSchema, DepartmentCreateRequestSchema, DepartmentUpdateRequestSchema

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)


@router.get("")
async def read_departments(
        department_service: Annotated[DepartmentService, Depends(get_department_service)],
        page: int = Query(1, ge=1),
        size: int = Query(50, ge=1, le=100),
        faculty_id: Optional[int] = None,
) -> Page[DepartmentReadResponseSchema]:
    return await department_service.get_departments(size=size, page=page, faculty_id=faculty_id)


@router.get("/{department_id}")
async def read_department(
        department_id: int,
        department_service: Annotated[DepartmentService, Depends(get_department_service)]
) -> DepartmentReadResponseSchema:
    return await department_service.get_department(department_id)


@router.post("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER]))])
async def create_department(
        request_schema: DepartmentCreateRequestSchema,
        department_service: Annotated[DepartmentService, Depends(get_department_service)],
) -> DepartmentReadResponseSchema:
    return await department_service.create_department(request_schema.model_dump())


@router.patch("/{department_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER]))])
async def update_department(
        department_id: int,
        request_schema: DepartmentUpdateRequestSchema,
        department_service: Annotated[DepartmentService, Depends(get_department_service)],
) -> DepartmentReadResponseSchema:
    return await department_service.update_department(department_id, request_schema.model_dump(exclude_unset=True))


@router.delete("/{department_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN]))])
async def delete_department(
        department_id: int,
        department_service: Annotated[DepartmentService, Depends(get_department_service)],
):
    return await department_service.delete_department(department_id)
