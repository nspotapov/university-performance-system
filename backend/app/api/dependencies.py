from app.repositories import UsersRepository
from app.services import UsersService


def get_users_service():
    return UsersService(UsersRepository)
