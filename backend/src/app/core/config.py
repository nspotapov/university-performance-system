import datetime
import secrets

from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False

    SECRET_KEY: str = secrets.token_urlsafe(32)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    PROJECT_NAME: str = "FastAPI"

    POSTGRES_PORT: int = 5432
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:  # noqa
        return "{}://{}:{}@{}:{}/{}".format(
            "postgresql+asyncpg",
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB
        )

    JWT_SECRET_KEY: str = secrets.token_urlsafe(512)
    JWT_ACCESS_TOKEN_EXPIRES_MINUTE: int = 15
    JWT_COOKIE_SECURE: bool = False
    JWT_COOKIE_HTTP_ONLY: bool = True
    JWT_COOKIE_CSRF_PROTECT: bool = False

    MFA_JWT_ACCESS_TOKEN_EXPIRES_MINUTE: int = 5
    MFA_JWT_SECRET_KEY: str = secrets.token_urlsafe(512)

    @computed_field
    @property
    def MFA_JWT_ACCESS_TOKEN_EXPIRES(self) -> datetime.timedelta:
        return datetime.timedelta(minutes=self.MFA_JWT_ACCESS_TOKEN_EXPIRES_MINUTE)

    @computed_field
    @property
    def JWT_ACCESS_TOKEN_EXPIRES(self) -> datetime.timedelta:
        return datetime.timedelta(minutes=self.JWT_ACCESS_TOKEN_EXPIRES_MINUTE)

    SMTP_HOST: str = "mailhog"
    SMTP_PORT: int = "8025"
    SMTP_USER: str = "user"
    SMTP_PASSWORD: str = "password"
    SMTP_FROM: str = "support@example.com"
    SMTP_TLS: bool = False


settings = Settings()  # noqa

__all__ = (
    "settings",
)
