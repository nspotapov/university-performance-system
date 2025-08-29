from app.managers.auth_manager import AuthManager
from app.repositories import UsersRepository, OTPRepository
from app.services import UsersService


def get_users_service():
    return UsersService(UsersRepository)


def get_auth_manager():
    return AuthManager(OTPRepository, UsersRepository)
