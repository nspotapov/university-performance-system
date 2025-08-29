import hashlib

from authx import AuthXConfig, AuthX

import app.config


def get_password_hash(password: str) -> str:
    return hashlib.sha512(password.encode()).hexdigest()


jwt_config = AuthXConfig(
    JWT_ALGORITHM=app.config.jwt_algorithm,
    JWT_SECRET_KEY=app.config.jwt_secret_key,
    JWT_TOKEN_LOCATION=app.config.jwt_token_location,
)

jwt_security = AuthX(config=jwt_config)
