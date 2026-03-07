from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.v1.dependencies import check_user_role, get_user_service
from app.api.v1.schemas import Page
from app.models import UserRole
from app.services import UserService
from .schemas import (
    UserReadResponseSchema, UserCreateRequestSchema, UserUpdateRequestSchema
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[
        Depends(check_user_role([UserRole.ADMIN]))
    ]
)


@router.get("")
async def read_users(
        user_service: Annotated[UserService, Depends(get_user_service)],
        page: int = Query(1, ge=1),
        size: int = Query(50, ge=1, le=100),
) -> Page[UserReadResponseSchema]:
    return await user_service.get_users(size=size, page=page)


@router.get("/{user_id}")
async def read_user(
        user_id: int,
        user_service: Annotated[UserService, Depends(get_user_service)]
) -> UserReadResponseSchema:
    return await user_service.get_user(user_id)


@router.post("")
async def create_user(
        request_schema: UserCreateRequestSchema,
        user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadResponseSchema:
    return await user_service.create_user(request_schema)


@router.patch("/{user_id}")
async def update_user(
        user_id: int,
        request_schema: UserUpdateRequestSchema,
        user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadResponseSchema:
    return await user_service.update_user(user_id, request_schema)


@router.delete("/{user_id}")
async def delete_user(
        user_id: int,
        user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.delete_user(user_id)
