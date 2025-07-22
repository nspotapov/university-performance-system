from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login")
async def authenticate_user():
    pass


@auth_router.post("/logout")
async def logout_user():
    pass
