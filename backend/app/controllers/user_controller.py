from pprint import pprint

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import config
from app.depends import get_session_without_commit, get_session_with_commit
from app.exceptions import ObjectNotFoundException
from app.models import User
from app.repositories import UserRepository
from app.schemas import UserSchema, UserCreateSchema, PaginationSchema
from app.schemas.user_schemas import UserUpdateSchema

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get("/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_session_without_commit)) -> UserSchema:
    user_repository = UserRepository(session)
    try:
        user = await user_repository.get(user_id)
        return UserSchema.model_validate(user)
    except ObjectNotFoundException:
        return status.HTTP_404_NOT_FOUND


@user_router.post("")
async def create_user(schema: UserCreateSchema, session: AsyncSession = Depends(get_session_with_commit)) -> UserSchema:
    user_repository = UserRepository(session)
    model = User(**schema.model_dump(exclude_unset=True))
    await user_repository.add(model)
    return status.HTTP_201_CREATED


@user_router.put("/{user_id}")
async def edit_user(user_id: int, schema: UserUpdateSchema,
                    session: AsyncSession = Depends(get_session_with_commit)) -> UserSchema:
    user_repository = UserRepository(session)
    try:
        rows_count = await user_repository.update(user_id, schema)
        if rows_count > 0:
            return status.HTTP_202_ACCEPTED
        else:
            raise ObjectNotFoundException
    except ObjectNotFoundException:
        return status.HTTP_404_NOT_FOUND


@user_router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session_with_commit)):
    user_repository = UserRepository(session)
    rows_count = await user_repository.delete(user_id)
    if rows_count == 1:
        return status.HTTP_202_ACCEPTED
    return status.HTTP_404_NOT_FOUND


@user_router.get("")
async def get_all_users(
        page: int = 1,
        limit: int = config.PAGINATION_DEFAULT_LIMIT,
        session: AsyncSession = Depends(get_session_without_commit)) -> PaginationSchema[UserSchema]:
    user_repository = UserRepository(session)
    users = await user_repository.get_all()

    users_count = len(users)
    pages_count = users_count // limit + min(users_count % limit, 1)

    page_obj = PaginationSchema(
        items=[UserSchema.model_validate(obj) for obj in users[(page - 1) * limit: (page - 1 + 1) * limit]],
        page=page,
        total_items=users_count,
        last_page=pages_count,
        total_pages=pages_count,
        items_by_page=limit,
        has_next_page=page < pages_count,
        has_prev_page=page > 1
    )
    return page_obj
