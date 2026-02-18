from typing import Type

import app.config
from app.common.security import jwt_security
from app.repositories import SQLAlchemyRepository, OTPRepository
from app.schemas.auth_schemas import AuthLoginSchema, AuthOTPLoginSchema
from app.schemas.user_schemas import UserReadSchema
from app.services import AuthService, OTPService, MailService


class AuthManager:
    def __init__(self, otp_repo: Type[OTPRepository], users_repo: Type[SQLAlchemyRepository]):
        self._auth_service = AuthService(users_repo)
        self._otp_service = OTPService(otp_repo)
        self._mail_service = MailService()

    async def login_user(self, schema: AuthLoginSchema) -> UserReadSchema | None:
        user = await self._auth_service.login_user(schema)

        if user is None:
            return None

        otp = await self._otp_service.create_otp_code(user.id)

        msg_text = f"Ваш код подтверждения: {otp.code}\n\nКод действителен {app.config.otp_code_expired_time} минут"
        msg_subject = "Подтверждение входа на портале университета"

        await self._mail_service.send_mail(user.email, msg_subject, msg_text)

        return user

    async def login_otp(self, schema: AuthOTPLoginSchema) -> str | None:
        user = await self._auth_service.login_user(schema)

        if user is None:
            return None

        is_verified = await self._otp_service.verify_otp_code(user.id, schema.otp_code, delete_code=True)

        if not is_verified:
            return None

        token = jwt_security.create_access_token(uid=str(user.id))

        return token
