import asyncio
import logging

from app.api.v1.users.schemas import UserCreateRequestSchema
from app.core.exceptions import ApplicationException
from app.db.session import async_session_maker
from app.models import UserRole
from app.services import UserService


async def main():
    async with async_session_maker() as db_session:
        user_service = UserService(db_session)
        try:
            await user_service.create_user(
                UserCreateRequestSchema(
                    email="admin@example.com",  # noqa
                    password="admin",
                    role=UserRole.ADMIN,
                )
            )
        except ApplicationException as ex:
            logging.warning(ex)


if __name__ == "__main__":
    asyncio.run(main())
