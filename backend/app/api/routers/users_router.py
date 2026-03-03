from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from fastapi import HTTPException

from app.api.dependencies import get_users_service, get_authorized_user, check_role
from app.common.security import jwt_security
from app.db.enums.user_role import UserRole
from app.exceptions import ApplicationException
from app.schemas.user_schemas import UserCreateSchema, UserReadSchema
from app.services import UsersService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_user(
        user: UserCreateSchema,
        users_service: Annotated[UsersService, Depends(get_users_service)],
) -> UserReadSchema:
    try:
        return await users_service.add_user(user)
    except ApplicationException as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(ex))


@router.get("", dependencies=[Depends(jwt_security.access_token_required)])
async def get_users(
        users_service: Annotated[UsersService, Depends(get_users_service)],
        current_user: Annotated[UserReadSchema, Depends(check_role([UserRole.ADMIN]))],
) -> List[UserReadSchema]:
    users = await users_service.get_users()
    return users


@router.get("/me")
async def get_current_user(current_user: Annotated[UserReadSchema, Depends(get_authorized_user)]) -> UserReadSchema:
    return current_user
