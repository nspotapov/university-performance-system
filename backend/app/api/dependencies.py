from app.managers.auth_manager import AuthManager
from app.repositories import UsersRepository, OTPRepository
from app.services import UsersService, AuthService, OTPService, MailService


def get_users_service():
    return UsersService(UsersRepository)

def get_auth_service():
    return AuthService(UsersRepository)

def get_otp_service():
    return OTPService(OTPRepository)

def get_mail_service():
    return MailService()

def get_auth_manager():
    return AuthManager(OTPRepository, UsersRepository)
