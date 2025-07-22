from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from .base_repository import BaseRepository
from ..schemas import UserSchema, UserCreateSchema


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=User)
