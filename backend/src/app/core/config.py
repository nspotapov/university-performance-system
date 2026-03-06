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
    JWT_TOKEN_LOCATION: list[str] = ["headers", "cookies"]
    JWT_COOKIE_SECURE: bool = False if DEBUG else True
    JWT_COOKIE_HTTP_ONLY: bool = True
    JWT_COOKIE_CSRF_PROTECT: bool = True

    MFA_JWT_EXPIRE_MINUTES: int = 5
    MFA_JWT_SECRET_KEY: str = secrets.token_urlsafe(512)

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
