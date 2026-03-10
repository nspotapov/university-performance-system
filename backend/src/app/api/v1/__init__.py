from fastapi import APIRouter

from .auth.router import router as auth
from .users.router import router as users

router = APIRouter(
    prefix="/v1",
)

routers = (
    auth,
    users,
)

for item in routers:
    router.include_router(item)

__all__ = (
    "router"
)
