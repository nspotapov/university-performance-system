import secrets
import pyotp
from datetime import datetime, timedelta
from authx import AuthXConfig, AuthX
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

from app.core.config import settings

password_hash = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher(),
    )
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    result = password_hash.verify_and_update(plain_password, hashed_password)
    return result[0] if result else False


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


# TOTP (Google Authenticator) functions
def generate_totp_secret() -> str:
    """Генерация секрета для TOTP"""
    return pyotp.random_base32()


def get_totp_uri(secret: str, email: str) -> str:
    """Получение URI для настройки Google Authenticator"""
    return pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name=settings.PROJECT_NAME)


def verify_totp_code(secret: str, code: str, window: int = 1) -> bool:
    """
    Проверка TOTP кода из Google Authenticator
    window - количество секунд до/после текущего времени для проверки (защита от рассинхронизации)
    """
    if not secret:
        return False
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=window)


# OTP (Email) functions
def generate_otp_code() -> str:
    """Генерация OTP кода (6 цифр)"""
    return ''.join([secrets.choice('0123456789') for _ in range(settings.OTP_CODE_LENGTH)])


def verify_otp_code(stored_code: str, stored_expire: datetime, user_code: str) -> bool:
    """
    Проверка OTP кода из email
    stored_code - сохраненный код
    stored_expire - время истечения кода
    user_code - код введенный пользователем
    """
    if not stored_code or not stored_expire:
        return False
    if datetime.utcnow() > stored_expire:
        return False
    return secrets.compare_digest(stored_code, user_code)


# JWT Security configurations
jwt_config = AuthXConfig(
    JWT_SECRET_KEY=settings.JWT_SECRET_KEY,
    JWT_ACCESS_TOKEN_EXPIRES=settings.JWT_ACCESS_TOKEN_EXPIRES,
    JWT_COOKIE_SECURE=settings.JWT_COOKIE_SECURE,
    JWT_COOKIE_HTTP_ONLY=settings.JWT_COOKIE_HTTP_ONLY,
    JWT_COOKIE_CSRF_PROTECT=settings.JWT_COOKIE_CSRF_PROTECT,
    JWT_ALGORITHM="HS256",
)

jwt_security = AuthX(config=jwt_config)

mfa_jwt_config = AuthXConfig(
    JWT_SECRET_KEY=settings.MFA_JWT_SECRET_KEY,
    JWT_ACCESS_TOKEN_EXPIRES=settings.MFA_JWT_ACCESS_TOKEN_EXPIRES,
    JWT_COOKIE_SECURE=settings.JWT_COOKIE_SECURE,
    JWT_COOKIE_HTTP_ONLY=settings.JWT_COOKIE_HTTP_ONLY,
    JWT_COOKIE_CSRF_PROTECT=settings.JWT_COOKIE_CSRF_PROTECT,
    JWT_ALGORITHM="HS256",
)

mfa_jwt_security = AuthX(config=mfa_jwt_config)


__all__ = (
    "verify_password",
    "get_password_hash",
    "get_totp_uri",
    "verify_totp_code",
    "generate_totp_secret",
    "generate_otp_code",
    "verify_otp_code",
    "jwt_security",
    "mfa_jwt_security",
)
