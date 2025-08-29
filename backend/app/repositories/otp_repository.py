import uuid

import redis.asyncio as redis

import app.config
import app.config
from app.schemas.otp_schemas import OTPReadSchema


class OTPRepository:
    def __init__(self):
        self._redis = redis.Redis(
            host=app.config.redis_host,
            port=app.config.redis_port,
            username=app.config.redis_username,
            password=app.config.redis_password,
            decode_responses=True
        )

    async def add_one(self, user_id: int, code: str) -> OTPReadSchema:
        key = ":".join(["user", str(user_id), "otp_code", str(uuid.uuid4())])
        await self._redis.setex(key, app.config.otp_code_expired_time * 60, code)
        return OTPReadSchema(id=key, user_id=user_id, code=code)

    async def find_all(self, user_id: int) -> list[OTPReadSchema]:
        key = ":".join(["user", str(user_id), "otp_code", "*"])

        otp_codes = []

        async for key in self._redis.scan_iter(key):
            code = await self._redis.get(key)
            otp_codes.append(OTPReadSchema(id=key, user_id=user_id, code=code))

        return otp_codes

    async def delete_one(self, id: str):
        await self._redis.delete(id)
