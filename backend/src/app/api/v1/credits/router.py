from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from app.api.v1.dependencies import check_user_role, get_credit_service
from app.api.v1.schemas import Page
from app.api.v1.academic.schemas import CreditReadResponseSchema, CreditCreateRequestSchema, CreditUpdateRequestSchema
from app.models import UserRole
from app.services import CreditService

router = APIRouter(prefix="/credits", tags=["Credits"])

@router.get("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER, UserRole.STUDENT]))])
async def read_credits(service: Annotated[CreditService, Depends(get_credit_service)], page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=100), student_id: Optional[int] = None, discipline_id: Optional[int] = None, semester_id: Optional[int] = None, teacher_id: Optional[int] = None, is_passed: Optional[bool] = None) -> Page[CreditReadResponseSchema]:
    return await service.get_credits(size=size, page=page, student_id=student_id, discipline_id=discipline_id, semester_id=semester_id, teacher_id=teacher_id, is_passed=is_passed)

@router.get("/{credit_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER, UserRole.STUDENT]))])
async def read_credit(credit_id: int, service: Annotated[CreditService, Depends(get_credit_service)]) -> CreditReadResponseSchema:
    return await service.get_credit(credit_id)

@router.post("", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER]))])
async def create_credit(request_schema: CreditCreateRequestSchema, service: Annotated[CreditService, Depends(get_credit_service)]) -> CreditReadResponseSchema:
    return await service.create_credit(request_schema.model_dump())

@router.patch("/{credit_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER, UserRole.TEACHER]))])
async def update_credit(credit_id: int, request_schema: CreditUpdateRequestSchema, service: Annotated[CreditService, Depends(get_credit_service)]) -> CreditReadResponseSchema:
    return await service.update_credit(credit_id, request_schema.model_dump(exclude_unset=True))

@router.delete("/{credit_id}", dependencies=[Depends(check_user_role([UserRole.ADMIN, UserRole.RECTOR, UserRole.DEAN, UserRole.HEAD_TEACHER]))])
async def delete_credit(credit_id: int, service: Annotated[CreditService, Depends(get_credit_service)]): return await service.delete_credit(credit_id)
