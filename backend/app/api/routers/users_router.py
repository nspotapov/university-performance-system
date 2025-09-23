from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from authx import TokenPayload

from app.api.dependencies import get_users_service
from app.common.security import jwt_security
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
    new_user = await users_service.add_user(user)
    return new_user


@router.get("", dependencies=[Depends(jwt_security.access_token_required)])
async def get_users(
        users_service: Annotated[UsersService, Depends(get_users_service)],
) -> List[UserReadSchema]:
    users = await users_service.get_users()
    return users


@router.get("/current")
async def get_current_user(
        users_service: Annotated[UsersService, Depends(get_users_service)],
        access_token_payload: TokenPayload = Depends(jwt_security.access_token_required),
) -> UserReadSchema:
    return await users_service.get_user(int(access_token_payload.sub))
