from fastapi import APIRouter

from .auth import router as auth

router = APIRouter(
    prefix="/v1",
)

router.include_router(auth)

__all__ = (
    "router"
)
