from fastapi import APIRouter

from .v1 import router as v1

router = APIRouter(
    prefix="/api",
)

@router.get("/health")
async def get_health():
    return {"status": "healthy"}

router.include_router(v1)

__all__ = (
    "router"
)
