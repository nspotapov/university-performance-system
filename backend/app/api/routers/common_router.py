from fastapi import APIRouter

router = APIRouter(
    prefix="/common",
    tags=["Common"],
)


@router.get("/healthcheck")
async def get_healthcheck() -> None:
    return "ok"
