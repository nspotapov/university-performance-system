import pyotp
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
    return password_hash.verify_and_update(plain_password, hashed_password)[0]


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def generate_totp_secret() -> str:
    return pyotp.random_base32()


def verify_totp_code(secret: str, code: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(code)


def get_totp_uri(secret: str, email: str) -> str:
    return pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name=settings.PROJECT_NAME)

jwt_config = AuthXConfig(
    JWT_SECRET_KEY=settings.JWT_SECRET_KEY,
    JWT_TOKEN_LOCATION=settings.JWT_TOKEN_LOCATION,
    JWT_COOKIE_SECURE=settings.JWT_COOKIE_SECURE,
    JWT_COOKIE_HTTP_ONLY=settings.JWT_COOKIE_HTTP_ONLY,
    JWT_COOKIE_CSRF_PROTECT=settings.JWT_COOKIE_CSRF_PROTECT,
)

jwt_security = AuthX(config=jwt_config)

mfa_jwt_config = AuthXConfig(
    JWT_SECRET_KEY=settings.MFA_JWT_SECRET_KEY,
    JWT_TOKEN_LOCATION=settings.JWT_TOKEN_LOCATION,
    JWT_COOKIE_SECURE=settings.JWT_COOKIE_SECURE,
    JWT_COOKIE_HTTP_ONLY=settings.JWT_COOKIE_HTTP_ONLY,
    JWT_COOKIE_CSRF_PROTECT=settings.JWT_COOKIE_CSRF_PROTECT,
)

mfa_jwt_security = AuthX(config=mfa_jwt_config)


__all__ = (
    "verify_password",
    "get_password_hash",
    "get_totp_uri",
    "verify_totp_code",
    "generate_totp_secret",
    "jwt_security",
    "mfa_jwt_security",
)
