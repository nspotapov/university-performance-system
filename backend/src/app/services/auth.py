from datetime import datetime, timedelta
from typing import Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.users.schemas import UserReadResponseSchema
from app.core import messages
from app.core.exceptions import ApplicationException
from app.core.security import (
    verify_password,
    verify_totp_code,
    generate_totp_secret,
    generate_otp_code,
    verify_otp_code,
)
from app.core.config import settings
from app.models import User, MFAMethod, UserRole
from app.repositories import UserRepository
from app.services.mail import MailService


class AuthService:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session
        self.__user_repository = UserRepository(db_session)
        self.__mail_service = MailService()

    async def login_user(self, email: str, password: str) -> Optional[UserReadResponseSchema]:
        """Вход пользователя по email и паролю"""
        users, _ = await self.__user_repository.find_all(email=email)
        if not users:
            return None
        
        user = users[0]
        if not verify_password(password, user.hashed_password):
            return None
        
        return UserReadResponseSchema.model_validate(user)

    def is_mfa_required(self, user: UserReadResponseSchema) -> bool:
        """Проверка обязательности 2FA для роли пользователя"""
        return UserRole.is_mfa_required(user.role)

    def should_require_mfa_on_login(self, user: UserReadResponseSchema) -> bool:
        """
        Проверка нужно ли требовать 2FA при входе
        - Для ADMIN, RECTOR, DEAN, HEAD_TEACHER, TEACHER - 2FA обязательна
        - Для STUDENT - 2FA опциональна (только если включена пользователем)
        """
        if UserRole.is_mfa_required(user.role):
            # Для этих ролей 2FA обязательна, проверяем включена ли она
            return not user.is_mfa_enabled
        else:
            # Для STUDENT 2FA опциональна
            return False

    async def verify_totp_code(self, user: UserReadResponseSchema, code: str) -> bool:
        """Проверка TOTP кода из Google Authenticator"""
        if not user.totp_secret:
            return False
        return verify_totp_code(user.totp_secret, code)

    async def verify_otp_code(self, user: UserReadResponseSchema, code: str) -> bool:
        """Проверка OTP кода из email"""
        if not user.otp_code or not user.otp_expires_at:
            return False
        
        # Проверяем код и обновляем время истечения
        is_valid = verify_otp_code(user.otp_code, user.otp_expires_at, code)
        
        if is_valid:
            # Очищаем OTP код после успешной проверки
            await self.__user_repository.update(user.id, {
                "otp_code": None,
                "otp_expires_at": None
            })
            await self.__db_session.commit()
        
        return is_valid

    async def send_otp_code(self, user: UserReadResponseSchema) -> str:
        """Генерация и отправка OTP кода на email"""
        otp_code = generate_otp_code()
        expire_time = datetime.utcnow() + timedelta(minutes=settings.OTP_CODE_EXPIRE_MINUTES)
        
        # Сохраняем код в БД
        await self.__user_repository.update(user.id, {
            "otp_code": otp_code,
            "otp_expires_at": expire_time
        })
        await self.__db_session.commit()
        
        # Отправляем email
        await self.__mail_service.send_mail(
            to_addrs=user.email,
            subject=f"Код подтверждения для {settings.PROJECT_NAME}",
            content=f"Ваш код подтверждения: {otp_code}\n\nКод действителен {settings.OTP_CODE_EXPIRE_MINUTES} минут."
        )
        
        return otp_code

    async def setup_totp(self, user: UserReadResponseSchema) -> Tuple[str, str]:
        """
        Настройка TOTP для пользователя
        Возвращает (secret, qr_code_uri)
        """
        secret = generate_totp_secret()
        qr_code_uri = generate_totp_secret_uri(secret, user.email)
        
        # Сохраняем секрет (но не включаем 2FA пока пользователь не подтвердит)
        await self.__user_repository.update(user.id, {
            "totp_secret": secret,
            "mfa_method": MFAMethod.TOTP
        })
        await self.__db_session.commit()
        
        return secret, qr_code_uri

    async def enable_totp(self, user: UserReadResponseSchema, code: str) -> bool:
        """Включение TOTP после проверки первого кода"""
        if not user.totp_secret:
            return False
        
        if verify_totp_code(user.totp_secret, code):
            await self.__user_repository.update(user.id, {
                "is_mfa_enabled": True,
                "mfa_method": MFAMethod.TOTP
            })
            await self.__db_session.commit()
            return True
        return False

    async def enable_otp(self, user: UserReadResponseSchema) -> bool:
        """Включение OTP (email) аутентификации"""
        await self.__user_repository.update(user.id, {
            "is_mfa_enabled": True,
            "mfa_method": MFAMethod.OTP
        })
        await self.__db_session.commit()
        return True

    async def disable_mfa(self, user: UserReadResponseSchema, password: str) -> bool:
        """Отключение MFA (требуется подтверждение паролем)"""
        if not verify_password(password, user.hashed_password):
            return False
        
        await self.__user_repository.update(user.id, {
            "is_mfa_enabled": False,
            "totp_secret": None,
            "otp_code": None,
            "otp_expires_at": None
        })
        await self.__db_session.commit()
        return True

    async def check_mfa_enabled(self, user: UserReadResponseSchema) -> bool:
        return user.is_mfa_enabled

    async def get_user_mfa_method(self, user: UserReadResponseSchema) -> MFAMethod:
        return user.mfa_method

    async def check_totp_enabled(self, user: UserReadResponseSchema) -> bool:
        return user.is_mfa_enabled and user.mfa_method == MFAMethod.TOTP

    async def check_user_is_active(self, user: UserReadResponseSchema) -> bool:
        return user.is_active

    async def get_user_with_refresh(self, user_id: int) -> Optional[UserReadResponseSchema]:
        """Получение пользователя для refresh токена"""
        user = await self.__user_repository.read(user_id)
        if not user:
            return None
        return UserReadResponseSchema.model_validate(user)


def generate_totp_secret_uri(secret: str, email: str) -> str:
    """Генерация URI для QR кода Google Authenticator"""
    return pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name=settings.PROJECT_NAME)


# Import pyotp here to avoid circular import
import pyotp
