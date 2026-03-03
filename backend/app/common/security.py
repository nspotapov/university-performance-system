import bcrypt
from authx import AuthXConfig, AuthX

import app.config


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


jwt_config = AuthXConfig(
    JWT_ALGORITHM=app.config.jwt_algorithm,
    JWT_SECRET_KEY=app.config.jwt_secret_key,
    JWT_TOKEN_LOCATION=app.config.jwt_token_location,
    JWT_JSON_KEY=app.config.jwt_json_key,
    JWT_REFRESH_JSON_KEY=app.config.jwt_refresh_json_key,
    JWT_COOKIE_SECURE=app.config.jwt_cookie_secure,
    JWT_HEADER_NAME=app.config.jwt_header_name,
    JWT_HEADER_TYPE=app.config.jwt_header_type,
)

jwt_security = AuthX(config=jwt_config)
