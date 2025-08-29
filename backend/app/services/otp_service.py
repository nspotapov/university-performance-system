import random
from typing import Type

from app.repositories import OTPRepository
from app.schemas.otp_schemas import OTPReadSchema


class OTPService:
    def __init__(self, otp_repo: Type[OTPRepository]):
        self.otp_repo: OTPRepository = otp_repo()

    async def create_otp_code(self, user_id: int) -> OTPReadSchema:
        code = str(random.randint(1000, 9999))
        return await self.otp_repo.add_one(user_id, code)

    async def verify_code(self, user_id: int, code: str) -> bool:
        user_otp_codes = await self.otp_repo.find_all(user_id=user_id)

        for user_otp_code in user_otp_codes:
            if user_otp_code.code == code:
                await self.otp_repo.delete_one(user_otp_code.id)
                return True

        return False
