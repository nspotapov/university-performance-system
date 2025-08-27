from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.api.dependencies import get_users_service
from app.schemas.user_schemas import UserCreateSchema, UserReadSchema
from app.services import UsersService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("")
async def add_user(
        user: UserCreateSchema,
        users_service: Annotated[UsersService, Depends(get_users_service)],
) -> UserReadSchema:
    new_user = await users_service.add_user(user)
    return new_user


@router.get("")
async def get_users(
        users_service: Annotated[UsersService, Depends(get_users_service)],
) -> List[UserReadSchema]:
    users = await users_service.get_users()
    return users
